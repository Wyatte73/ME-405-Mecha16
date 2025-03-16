import gc
import pyb
import cotask, task_share

import motor, encoder, pid, time, os, line
from imu import IMU
from pyb import Pin, Timer, I2C, ExtInt
from math import pi, copysign
from nb_input import NB_Input

# Sets up the Bluetooth Module in UART5
uart = pyb.UART(5,460800)
pyb.repl_uart(uart)
nb_in = NB_Input (uart, echo=True)

# Physical Parameters of Romi
r_w = 3.5  # [cm]
w   = 14.1 # [cm]

'''
   Defining the motor control task
   In this task the v_set, yaw_rate, Om_set, and run_flg shares are received
   and used to alter the effort of the PWM that drives our motors.
   
   v_set: the base velocity Romi should drive forward with during the entirety
   of the course. Can be scaled within certain sections
   
   yaw_rate: the yaw rate that the Romi must turn at to hold its course
   based off of input from the sensors. This then gets sent to the motor 
   control and run through the control loop.
'''
class MOTOR_CONTROL:
    def __init__(self):
        # Initiates our motors ans drivers within their respective drivers
        self.Lmot = motor.Motor(Pin.cpu.A15, Pin.cpu.C10, Pin.cpu.C11, Timer(2, freq=50000), 1)
        self.Rmot = motor.Motor(Pin.cpu.B6, Pin.cpu.C8, Pin.cpu.C6, Timer(4, freq=50000), 1)
        self.Lenc = encoder.Encoder(1, Pin.cpu.A8, 2, Pin.cpu.A9, 1)
        self.Renc = encoder.Encoder(1, Pin.cpu.B4, 2, Pin.cpu.B5, 3)
        
    def task(self, shares):
        # Defining state names and zeroing necissary variables
        S0_Init                = 0
        S1_Waiting_For_Run_Flg = 1
        S2_Run_Motors          = 2
        S3_Reset               = 3
        velocity               = 0
        state                  = S0_Init
        
        # Import shares
        yaw_rate, Om_set, v_set = shares
   
        while True:            
            if state == S0_Init:
                # In the init state, enable the motors but set them to 0%
                # effort
                self.Lmot.enable()
                self.Rmot.enable()
                self.Lmot.set_effort(0)
                self.Rmot.set_effort(0)
               
                # C1 and C2 are instances of the PID method with different
                # values for Kp, Ki, and Kd. C2 is used for the yaw rate and
                # C1 is for the angular velocity of the wheels
                C2 = pid.PID(8,0,0)
                C1 = pid.PID(.1,0,0)
                
                # Zero necissary variables
                yaw_rate_input = 0
                yaw_rate_req = 0
                state = S1_Waiting_For_Run_Flg
               
            elif state == S1_Waiting_For_Run_Flg:         
                # If the run flag is set high, update and zero the motors then
                # set the state to state 2.
                if run_flg.get() == 1:
                    self.Lenc.update()
                    self.Renc.update()
                    self.Lenc.zero()
                    self.Renc.zero()
                    state = S2_Run_Motors
                   
            elif state == S2_Run_Motors:                
                # If run flag is low, reset
                if run_flg.get() == 0:
                    state = S3_Reset

                elif run_flg.get() == 1:                  
                    # Speed scaling for corners, but only run this speed 
                    # scaling after section 1 because section 1 is dealt with
                    # specially in its own task
                    if section.get() == 1: 
                        velocity = v_set.get()
                    else:
                        if abs(yaw_rate.get()) >= 4:
                            velocity = 0.7*v_set.get()
                        else:
                            velocity = v_set.get()
                            
                    # Control loop that takes in shares from the sensors and 
                    # returns a new efforst for the motors
                    yaw_rate_input = Om_set.get() - yaw_rate.get()
                    yaw_rate_req = C2.control(yaw_rate_input)
                   
                    Om_L = velocity / r_w - w * yaw_rate_req / (2 * r_w)
                    Om_R = velocity / r_w + w * yaw_rate_req / (2 * r_w)
                   
                    Om_L_input = Om_L - self.Lenc.get_velocity() * 2 * pi / 1440
                    Om_R_input = Om_R - self.Renc.get_velocity() * 2 * pi / 1440
                   
                    Om_L_output = C1.control(Om_L_input)
                    Om_R_output = C1.control(Om_R_input)
                   
                    # Conversion from rad/s to effor based on left motor testing
                    Om_L_gain = Om_L_output * 100 / (4.11 * 7.2) 
                    # Conversion from rad/s to effor based on right motor testing
                    Om_R_gain = Om_R_output * 100 / (3.36 * 7.2) 
                   
                    self.Lmot.set_effort(velocity + int(Om_L_gain))
                    self.Rmot.set_effort(velocity + int(Om_R_gain))
                   
                    self.Lenc.update()
                    self.Renc.update()
                                       
            elif state == S3_Reset:
                self.Lmot.set_effort(0)
                self.Rmot.set_effort(0)
                self.Lenc.zero()
                self.Renc.zero()
                state = S1_Waiting_For_Run_Flg
                   
            yield 0    

# Sensor class with functions for all three sensors: IMU, IR line sensor, and
# bump sensor
class SENSORS:
    def __init__(self):        
        # Initialization and calibration for line sensor
        self.line_sen = line.Line(Pin.cpu.C2, Pin.cpu.C3, Pin.cpu.C0, Pin.cpu.C1, Pin.cpu.B0, Pin.cpu.A1, Pin.cpu.A0, Pin.cpu.A6, Pin.cpu.A7, Pin.cpu.B1)
        self.line_sen.calibration()
        self.center_sensor = 8
       
        # Initialization for encoders and motors
        self.Lmot = motor.Motor(Pin.cpu.A15, Pin.cpu.C10, Pin.cpu.C11, Timer(2, freq=50000), 1)
        self.Rmot = motor.Motor(Pin.cpu.B6, Pin.cpu.C8, Pin.cpu.C6, Timer(4, freq=50000), 1)
        self.Lenc = encoder.Encoder(1, Pin.cpu.A8, 2, Pin.cpu.A9, 1)
        self.Renc = encoder.Encoder(1, Pin.cpu.B4, 2, Pin.cpu.B5, 3)
       
        # Initialization and calibration for IMU
        i2c = I2C(1, mode=I2C.CONTROLLER)
        self.imu = IMU(i2c)
        self.imu.set_mode(0x00) 
        # Sets to IMU mode. 0x0C is NDOF mode, 0x08 is IMU mode
        # Based on current code setup. Must be in NDOF mode to calibrate IMU
        self.imu.set_mode(0x08)  
        time.sleep(0.25)
        self.heading = 0
              
        # If a calibration file exist, load that file into the IMU. If not,
        # perform calibrating and save those coefficients when complete
        if "calibration.txt" in os.listdir():
            print("Loading calibration data...")
            self.imu.set_calibration_coefficients()
        else:
            print("Performing manual calibration...")
            while True:
                status =  self.imu.get_calibration_status()
                print(f"Calibration: {status}")
                if all(val == 3 for val in status.values()):
                    self.imu.get_calibration_coefficients()           
                    break
                time.sleep(1)
           
    def IMU(self, shares):
        yaw_rate, v_set, heading_set, section, bump_flg = shares
        count      = 0
        set_path   = 1
        SEC5_S0    = 0
        SEC5_S1    = 1
        SEC5_S2    = 2
        SEC5_S3    = 3
        SEC5_S4    = 4
        SEC5_S5    = 5
        state      = 0
        
        # On first pass, set the heading setpoint to the current heading 
        # (Romi begins pointing "North"). Additionally, create a copy of v_set
        # so the original value is preserved even when new v_set values are 
        # assigned.
        heading_set.put(self.imu.get_heading())
        self.v_set_temp = v_set.get()     
       
        while True:
            # Update encoder and get position every pass through
            self.Lenc.update()
            position = self.Lenc.get_position()
            
            # Section 2 is the short section where the IMU guides Romi
            # straight through the diamond.
            if section.get() == 2:  
                # For first pass through only, set endpoint in cm
                if set_path == 1:
                    start = position
                    diamond_end = start + 20 * 1440 / (2 * pi * 3.5) # 20cm
                    set_path = 0   
                
                # If Romi has not reached the endpoint, continue to drive and 
                # correct heading
                if position < diamond_end:  
                    print("In section 2")
                    heading = self.imu.get_heading()
                    # Error for aiming east (90 degrees)
                    err = ((heading_set.get() + 90) - heading + 180) % 360 - 180
                    # Conversion for yaw rate that accomplished two things:
                        # 1: makes yaw rate a similar magnitude as a 
                        # comparable turn guided by the line sensor
                        # 2: adds a small base value to overcome friction
                    yaw_rate.put(err/10 + .5*copysign(1, err))
                    # Only go 70% speed
                    v_set.put(0.7*self.v_set_temp)
                
                # Once the endpoint has been reached, set v_set for next 
                # section, moved to next section, and reinitialize some
                # variables
                else:
                    count = 0
                    set_path = 1
                    section.put(3)  
                    v_set.put(0.85*self.v_set_temp)
            
            # Section 5.0 is when Romi drives south on the grid       
            elif section.get() == 5:            
                if state == SEC5_S0:
                    print("In section 5.0")
                    if set_path == 1:
                        start = position
                        south_end = start + 60 * 1440 / (2 * pi * 3.5) # 60cm
                        set_path = 0    
                   
                    if position < south_end:            
                        heading = self.imu.get_heading()
                        # Error for aiming south
                        err = ((heading_set.get() + 180) - heading + 180) % 360 - 180
                        yaw_rate.put(err/10 + .5*copysign(1, err))
                        # Straight line so we want Romi to go fast
                        v_set.put(1.5*self.v_set_temp)
                        
                    else:
                        count = 0
                        set_path = 1
                        state = SEC5_S1
                       
                # Section 5.1 is when Romi drives west towards the wall 
                elif state == SEC5_S1:
                    print("In section 5.1")
                    heading = self.imu.get_heading()
                    # No end point set because Romi must drive until it hits
                    # the wall
                    # Error for aiming west
                    err = ((heading_set.get() + 270) - heading + 180) % 360 - 180
                    yaw_rate.put(err/10 + .5*copysign(1, err))
                   
                    # Give Romi 400ms second to point west before driving
                    if count < 40:
                        v_set.put(0)
                        count += 1
                    # If the bump flag sensor is set high, go to next state
                    # else drive at 70% speed (can't be breaking those bottons).
                    elif bump_flg.get() == 1:
                        v_set.put(0)
                        count = 0
                        state = SEC5_S2              
                    else:
                        v_set.put(0.7*self.v_set_temp)
                       
                # Section 5.2 is when Romi drives east backwarstowards to 
                # line up with the cup
                elif state == SEC5_S2:
                    print("In section 5.2")
                    if set_path == 1:
                        start = position
                        backup_end = start - 5 * 1440 / (2 * pi * 3.5) # 5cm
                        set_path = 0  
                   
                    if position > backup_end:            
                        heading = self.imu.get_heading()
                        # error for aiming west
                        err = ((heading_set.get() + 270) - heading + 180) % 360 - 180
                        yaw_rate.put(err/10 + .5*copysign(1, err))
                        v_set.put(-1.2*self.v_set_temp)
                       
                    else:
                        count = 0
                        set_path = 1
                        state = SEC5_S3
                       
                # Section 5.3 is when Romi drives turns north and 
                # drives to displace the cup closest to the start
                elif state == SEC5_S3:
                    print("In section 5.3")
                    if set_path == 1:
                        start = position
                        north_end = start + 40 * 1440 / (2 * pi * 3.5) # 40cm
                        set_path = 0           
                   
                    if position < north_end:            
                        heading = self.imu.get_heading()
                        # Error for aiming north
                        err = ((heading_set.get() + 0) - heading + 180) % 360 - 180
                        yaw_rate.put(err/10 + .5*copysign(1, err))
                       
                        # Give Romi 400ms second to point north
                        if count < 40:
                            v_set.put(0)
                            count += 1
                        else:    
                            v_set.put(1.2*self.v_set_temp)
                    else:
                        count = 0
                        set_path = 1
                        state = SEC5_S4
                       
                # Section 5.4 is when Romi drives turns west and drives to the
                # very beginning of the track
                if state == SEC5_S4:
                    if set_path == 1:
                        start = position
                        west_end = start + 18 * 1440 / (2 * pi * 3.5) # 18cm
                        set_path = 0    
                   
                    if position < west_end:  
                        print("In section 5.4")
                        heading = self.imu.get_heading()
                        # Error for aiming west
                        err = ((heading_set.get() + 270) - heading + 180) % 360 - 180
                        yaw_rate.put(err/10 + .5*copysign(1, err))
                       
                        # Give Romi 400ms second to point west    
                        if count < 40:
                            v_set.put(0)
                            count += 1
                        else:    
                            v_set.put(1.2*self.v_set_temp)
                    else:
                        count = 0
                        set_path = 1
                        state = SEC5_S5
            
                # Section 5.5 is when Romi drives turns south and drives back
                # to the starting square
                if state == SEC5_S5:
                    print("In section 5.5")
                    if set_path == 1:
                        start = position
                        south_end = start + 27 * 1440 / (2 * pi * 3.5) # 27cm
                        set_path = 0    
                   
                    if position < south_end:            
                        heading = self.imu.get_heading()
                        # error for aiming south
                        err = ((heading_set.get() + 180) - heading + 180) % 360 - 180
                        yaw_rate.put(err/10 + .5*copysign(1, err))
                        
                        # Give Romi 400ms second to point south    
                        if count < 40:
                            v_set.put(0)
                            count += 1
                        else:    
                            v_set.put(self.v_set_temp)
                        
                    else:
                        count = 0
                        set_path = 1
                        run_flg.put(0)
                        section.put(6)
                
                # Section 6 signifies the completion of the course
                elif section.get() == 6: 
                    print("DONE")
                    
            yield 0                   
           
    def LINE(self, shares):
        run_flg, yaw_rate, Om_set, v_set, heading_set, section, bump_flg = shares
        self.v_set_temp = v_set.get() 
       
        while True:
            # Section 1 of the track. Line following which converts the
            # centroid location into a yaw rate to corret Romi's yaw angle.
            if section.get() == 1:
                self.line_sen.line_reading()
                center_sensor, white_sensors = self.line_sen.center()
                print("In section 1")
                if center_sensor > 0:              
                    yaw_rate.put(2*int((center_sensor - 8)))
                else:
                    yaw_rate.put(0)
                # If more black is detected than a regular line (the beginning
                # of the diamond) then go to section 2.
                if white_sensors < 6:
                    section.put(2)
                # If yaw rate is greater than 6 (the turn at the end of the 
                # straight) then slow down.
                if yaw_rate.get() > 6:
                    print("Sloowwwwwing Dowwwwwwwwn")
                    v_set.put(0.5*self.v_set_temp)
                                  
            # Section 3. Traditional line following.
            elif section.get() == 3:
                print("In section 3")
                self.line_sen.line_reading()
                center_sensor, white_sensors = self.line_sen.center()
                if center_sensor > 0:              
                    yaw_rate.put(int((center_sensor - 8)))
                else:
                    yaw_rate.put(0)
                # If more black is detected than a regular line (hash before
                # grid section) then go to section 4.
                if white_sensors < 2:
                    section.put(4)
           
            # Section 4. Traditional line following.
            elif section.get() == 4:
                print("In section 4")
                self.line_sen.line_reading()
                center_sensor, white_sensors = self.line_sen.center()
                if center_sensor > 0:              
                    yaw_rate.put(int((center_sensor - 8)))
                else:
                    yaw_rate.put(0)
                # If mostly white is detected (beginning fo the grid section),
                # then go to section 5.
                if white_sensors > 9:
                    section.put(5)    
                   
            else:
                pass
           
            yield 0
           
    def BUMP(self, shares):
        bump_flg = shares
        
        # Creates a list with all bumb sensors
        bump_sensor_pins = [
            Pin(Pin.cpu.A10, Pin.IN, Pin.PULL_UP),  # Sensor 0
            Pin(Pin.cpu.B3, Pin.IN, Pin.PULL_UP),   # Sensor 1
            Pin(Pin.cpu.C9, Pin.IN, Pin.PULL_UP),   # Sensor 2
            Pin(Pin.cpu.B12, Pin.IN, Pin.PULL_UP),  # Sensor 3
            Pin(Pin.cpu.B11, Pin.IN, Pin.PULL_UP),  # Sensor 4
            Pin(Pin.cpu.B2, Pin.IN, Pin.PULL_UP)    # Sensor 5
            ]
        
        while True:
            # If high, set low on next pass through
            if bump_flg.get() == 1:
                bump_flg.put(0)
                
            # Iterate though every pin and if any have been pressed, set the
            # bump flag to high
            else:
                for pin in bump_sensor_pins:
                    if pin.value() == 0:  # Assuming the sensor pulls LOW when activated
                        bump_flg.put(1)
                        break
   
            yield 0
            
# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
# A significant portion of this folloing code is from Dr. Ridgely's GitHub.
if __name__ == "__main__":
    # Initialize motors in main as well so we can set efforts to zero
    # immediately
    Lmot = motor.Motor(Pin.cpu.A15, Pin.cpu.C10, Pin.cpu.C11, Timer(2, freq=50000), 1)
    Rmot = motor.Motor(Pin.cpu.B6, Pin.cpu.C8, Pin.cpu.C6, Timer(4, freq=50000), 1)

    # Runs the init for the motor control and sensors classes 
    MOTOR_CONTROL = MOTOR_CONTROL()
    SENSORS = SENSORS()
    
    input("Press Enter when Romi is on starting square.")

    # Create a shares and queues for the sceduler
    yaw_rate = task_share.Share('f', thread_protect=False, name ="Yaw Rate")
    Om_set = task_share.Share('h', thread_protect=False, name ="Yaw Rate Setpoint")
    v_set = task_share.Share('f', thread_protect=False, name ="Longitudinal Velocity Setpoint")
    heading_set = task_share.Share('f', thread_protect=False, name ="Heading for North")
    section = task_share.Share('h', thread_protect=False, name ="Section")
    bump_flg = task_share.Share('h', thread_protect=False, name ="Bump Flag")  
    run_flg = task_share.Share('h', thread_protect=False, name ="Bump Flag")  
   
    # Set initial values for shares
    Om_set.put(0)
    v_set.put(50)
    heading_set.put(0)
    section.put(1)
    run_flg.put(1)
   
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for
    # debugging and set trace to False when it's not needed 
    task1 = cotask.Task(MOTOR_CONTROL.task, name="Task_1", priority=2, period=10,
                        profile=True, trace=False, shares=(yaw_rate, v_set))
    task2 = cotask.Task(SENSORS.IMU, name="Task_2", priority=3, period=10,
                        profile=True, trace=False, shares=(yaw_rate, v_set, heading_set, section, bump_flg))
    task3 = cotask.Task(SENSORS.LINE, name="Task_3", priority=4, period=10,
                        profile=True, trace=False, shares=(yaw_rate, v_set, section))
    task4 = cotask.Task(SENSORS.BUMP, name="Task_4", priority=1, period=10,
                        profile=True, trace=False, shares=(bump_flg))
   
    cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    cotask.task_list.append(task4)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        # except KeyboardInterrupt:
        #     Lmot.disable()
        #     Rmot.disable()
        #     print("Program Terminated")
        #     break
        except:
            Lmot.disable()
            Rmot.disable()
            raise
