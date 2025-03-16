# ME-405-Mecha16 Term Project
### Ethan Gray and Wyatt Eberhart

## Table of Contents
- [Project Overview](#projectoverview)
- [Hardware](#hardware)
- [Software](#software)

## Project Overview
- [Back to top](#Table-of-Contents)

This repository contains the ME-405 term project by Ethan Gray and Wyatt Eberhart. The objective of this project was to develop and implement a control system for a differential-drive robot, Romi, using MicroPython. Romi was programmed to autonomously navigate a predefined course (depicted in Figure 1) by utilizing three primary sensors: an inertial measurement unit (IMU), line sensors, and bump sensors. These sensors were integrated with the Romi chassis kit and combined with Pololu motors and a Pololu power distribution board. Figure 2 shows the final build of Romi.

The system was controlled using an STM32 Nucleo-L476RG development board, which served as the main processing unit. Task execution was managed through a real-time scheduler, ensuring periodic execution with designated priorities. Within these scheduled tasks, a finite state machine (FSM) was implemented to enable Romi to know what section of the track it was on and react accordingly.

<p align="center">
  <img width="1389" alt="Screenshot 2025-03-16 at 12 55 04 PM" src="https://github.com/user-attachments/assets/97ac74ea-d0b5-4674-859b-4bc7075b9cf2" />
</p>
<p align="center">
  Figure 1. Course Layout
</p>

<p align="center">
  <img width="600" alt="IMG_5718" src="https://github.com/user-attachments/assets/c376aa85-b766-441c-93ef-0afb0c2265a2" />
</p>
<p align="center">
  Figure 1. Course Layout
</p>

https://youtube.com/shorts/zJc4XDnnLkc

## Hardware
- [Back to top](#Table-of-Contents)
- [Romi Chassis and Components](#romi-chassis-and-components)
- [Microcontroller](#microcontroller)
- [Sensors](#sensors)
- [Additional Components](#additional-components)
- [Wiring Diagram](#wiring-diagram)

### Romi Chassis and Components
The main part of Romi from Pololu has the motors, encoders, power distribution board, and the chassis. The motors are connected to a gearbox with a 120:1 ratio. The encoders have a resolution of 12 ticks per revolution giving 1440 encoder ticks per revolution of the wheel. Romi takes 6 AA batteries to function properly which is handled through the power distribution board. The power to the motor is connected directly to the power distribution board and are controlled through the power distribution board.

<p align="center">
  <img width="350" alt="[Screenshot 2025-03-16 160101" src="https://github.com/user-attachments/assets/f1b07fd9-ac19-4c26-b4b9-96e414122c30" />
</p>
<p align="center">
  Figure ???. Romi Motor and Encoder Pair
</p>

<p align="center">
  <img width="450" alt="[Screenshot 2025-03-16 160153" src="https://github.com/user-attachments/assets/8af7760e-e74b-4c70-9e59-c029caaecfe0" />
</p>
<p align="center">
  Figure ???. Romi Power Distribution Board
</p>

<p align="center">
  <img width="450" alt="[Screenshot 2025-03-16 160208" src="https://github.com/user-attachments/assets/0ec7f4de-23a0-4646-b721-331e287d3c96" />
</p>
<p align="center">
  Figure ???. Romi Chassis
</p>

### Microcontroller
The microcontroller that was used was the STM32 Nucleo-L476RG. This was provided by the professor. This was the mind of Romi and was able to control Romi by obtaining the readings from the sensors. After interpreting the data, Romi was able to control the motors to traverse through the course.  Figure ??? shows the Nucleo Board.  

<p align="center">
  <img width="350" alt="[Screenshot 2025-03-16 142309" src="https://github.com/user-attachments/assets/ad4143ad-f2fc-4ce5-9881-01eb9068ed2d" />
</p>
<p align="center">
  Figure ???. Nucleo L476RG
</p>

### Sensors
The three main sensors used were an IMU, a line sensor, and bump sensors. The IMU was used to determine the heading of ROMI. The IMU has an accelerometer, gyroscope, and magnetometer, however, only the accelerometer and gyroscope were used during the final term project. This is because Romi was calibrated at the start of the course to find a local “north” direction that was used as a reference for any other direction. Figure ??? shows the IMU. The line sensor is an infrared sensor array with 15 sensors having a pitch of 4 mm. Due to the lack of ADC pins on the nucleo board, only 10 of the sensors were used. The sensors produce an analog output with the greater the output value, the more reflective the surface is. For the track, the black lines produced greater values which is how Romi was able to detect the lines. Figure ??? shows the line sensor that was used. The bump sensors were used to detect the wall towards the end of the track. They acted as a switch, either being off or on when the switch was depressed. Figure ??? shows the bump sensors that were used.

<p align="center">
  <img width="350" alt="[Screenshot 2025-03-16 132044" src="https://github.com/user-attachments/assets/75282655-6f3c-4acc-bebd-a26dc5f86d2b" />
</p>
<p align="center">
  Figure ???. BNO055 IMU
</p>

<p align="center">
  <img width="350" alt="[Screenshot 2025-03-16 124428" src="https://github.com/user-attachments/assets/87a4b780-bd74-4869-acef-98eb18fece45" />
</p>
<p align="center">
  Figure ???. QTR-HD-15A IR Sensor Array
</p>

<p align="center">
  <img width="350" alt="[Screenshot 2025-03-16 132123" src="https://github.com/user-attachments/assets/de5c8547-8330-4591-9034-422a7068c77a" />
</p>
<p align="center">
  Figure ???. Romi Bump Sensor
</p>

### Additional Components
A HC-05 bluetooth module was also implemented to be able to use the REPL over bluetooth. This wasn’t needed but was a nice feature to have. This removed the usb wire going from Romi to the computer. The HC-05 had to be reconfigured to rename and give the module a new password. The baudrate was also increased to 460800. Figure ??? shows the HC-05 bluetooth module that was used.

<p align="center">
  <img width="350" alt="[Screenshot 2025-03-16 132414" src="https://github.com/user-attachments/assets/7a990adc-fc7c-4450-bb18-58cdf33d645e" />
</p>
<p align="center">
  Figure ???. HC-05 Bluetooth Module
</p>

Standard mounting hardware was used and provided, but any way to mount the various sensors would suffice as long the sensors are mounted according to the manufacturer's specifications.

### Wiring Diagram

<p align="center">
  <img width="1093" alt="[Screenshot 2025-03-16 153800" src="https://github.com/user-attachments/assets/4b9bbbcd-4be2-4f62-b9b7-f1827ae09b97" />
</p>
<p align="center">
  Figure ???. Wiring Diagram
</p>

## Software
- [Back to top](#Table-of-Contents)
- [Hardware Drivers](#hardware-drivers)
- [Task Diagram](#task-diagram)


### Hardware Drivers

The repository contains the main program file and all necessary hardware driver modules. [main.py](./main.py) is responsible for initializing the hardware and drivers, setting up and executing the scheduler, and managing the finite state machine (FSM). The following driver modules provide hardware interfacing:

&nbsp;&nbsp;&nbsp;&nbsp;[encoder.py](./encoder.py) – Handles communication with the wheel encoders to measure position and velocity.  

&nbsp;&nbsp;&nbsp;&nbsp;[motor.py](./motor.py) – Controls the Pololu motors for precise actuation.  

&nbsp;&nbsp;&nbsp;&nbsp;[imu.py](./imu.py) – Interfaces with the inertial measurement unit (IMU) for orientation and motion sensing.  

&nbsp;&nbsp;&nbsp;&nbsp;[line.py](./line.py) – Processes input from the line sensors to detect track boundaries. 

&nbsp;&nbsp;&nbsp;&nbsp;[pid.py](./pid.py) – Implements a PID controller for motor speed regulation.

### Task Diagram

Task scheduling and shared variable management are implemented using cotask.py and task_share.py. The task diagram can be seen below in Figure _.A key limitation on task execution frequency is the resolution of the velocity measurements obtained from the encoders. Through testing, we determined that the maximum feasible task execution rate is approximately 100 Hz. Running all tasks at this frequency did not introduce any performance issues. The scheduler cycles through four tasks:

&nbsp;&nbsp;&nbsp;&nbsp;Motor Control (Priority: 2, Period: 10ms):

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Receives velocity and yaw rate inputs via shared variables.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Applies control algorithms and motor gains to determine the appropriate motor efforts.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Sends updated commands to the motors for precise actuation.

&nbsp;&nbsp;&nbsp;&nbsp;IMU Task (Priority: 3, Period 10ms):

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Manages approximately half of the FSM, handling sections that rely on IMU data (Sections 2 and 5.0–5.5).

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Communicates with the Line Sensor Task via the “section” share to ensure exclusive operation.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Receives input from the Bump Sensor Task to detect wall contact at the end of Section 5.1.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Computes and transmits updated velocity and yaw rate commands to the Motor Control Task based on heading information.

&nbsp;&nbsp;&nbsp;&nbsp;Line Sensor Task (Priority: 4, Period: 10ms):

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Controls the FSM for Sections 1, 3, and 4, processing line sensor data.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Shares control with the IMU Task through the “section” share..

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Computes the centroid of the detected line and transmits updated velocity and yaw rate commands to the Motor Control Task for course correction.

&nbsp;&nbsp;&nbsp;&nbsp;Bump Sensor Task (Priority 1, Period 10ms):

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- Solely responsible for detecting wall contact and setting a bump flag share high when a wall is detected.


<p align="center">
  <img width="445" alt="Screenshot 2025-03-14 at 12 37 26 PM" src="https://github.com/user-attachments/assets/b93a4060-abe6-48d0-a5c1-742849eac1dc" />
</p>
<p align="center">
  Figure _. Task Diagram
</p>
