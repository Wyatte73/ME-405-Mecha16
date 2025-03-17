# ME-405-Mecha16 Term Project

## Table of Contents
- [Project Overview](#projectoverview)
- [Hardware](#hardware)
  - [Romi Chassis and Components](#romi-chassis-and-components)
  - [Microcontroller](#microcontroller)
  - [Sensors](#sensors)
  - [Additional Components](#additional-components)
  - [Wiring Diagram](#wiring-diagram)
- [Software](#software)
  - [Hardware Drivers](#hardware-drivers)
  - [Task Diagram and FSM](#task-diagram-and-fsm)
  - [Gain Detirmination](#gain-detirmination)
- [Control Therory](#control-theory)
- [Getting Started](#getting-started)

## Project Overview
[Back to top](#Table-of-Contents)

This repository contains the ME-405 term project by Ethan Gray and Wyatt Eberhart. The objective of this project was to develop and implement a control system for a differential-drive robot, Romi, using MicroPython. Romi was programmed to autonomously navigate a predefined course (depicted in Figure 1) by utilizing three primary sensors: an inertial measurement unit (IMU), line sensors, and bump sensors. These sensors were integrated with the Romi chassis kit and combined with Pololu motors and a Pololu power distribution board. Figure 2 shows the final build of Romi.

The system was controlled using an STM32 Nucleo-L476RG development board, which served as the main processing unit. Task execution was managed through a real-time scheduler, ensuring periodic execution with designated priorities. Within these scheduled tasks, a finite state machine (FSM) was implemented to enable Romi to know what section of the track it was on and react accordingly.


<img height="280" alt="Screenshot 2025-03-16 at 12 55 04 PM" src="https://github.com/user-attachments/assets/97ac74ea-d0b5-4674-859b-4bc7075b9cf2" />
<img height="280" alt="IMG_5718" src="https://github.com/user-attachments/assets/c376aa85-b766-441c-93ef-0afb0c2265a2" />

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Figure 1. Course Layout
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Figure 2. Final Build of Romi

[![Watch the video](https://img.youtube.com/vi/zJc4XDnnLkc/maxresdefault.jpg)](https://www.youtube.com/shorts/zJc4XDnnLkc)
<p align="center">
  Click Thumbnail above to view demonstration
</p>

## Hardware
[Back to top](#Table-of-Contents)

### Romi Chassis and Components

The core components of Romi, sourced from Pololu, include the motors (Figure 5), encoders (Figure 5), power distribution board (Figure 3), and chassis (Figure 4). The motors are coupled with a 120:1 gearbox, providing high torque and precise control. Each encoder has a resolution of 12 ticks per motor shaft revolution, resulting in 1440 encoder ticks per full wheel rotation. Romi is powered by six AA batteries, which are regulated through the power distribution board. The motors receive power directly from the distribution board and are controlled through its integrated circuitry.


  <img height="240" alt="[Screenshot 2025-03-16 160153" src="https://github.com/user-attachments/assets/8af7760e-e74b-4c70-9e59-c029caaecfe0" />
  <img height="240" alt="[Screenshot 2025-03-16 160208" src="https://github.com/user-attachments/assets/0ec7f4de-23a0-4646-b721-331e287d3c96" />
  <img height="240" alt="[Screenshot 2025-03-16 160101" src="https://github.com/user-attachments/assets/f1b07fd9-ac19-4c26-b4b9-96e414122c30" />

&nbsp;&nbsp;
Figure 3. Power Distribution Board
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Figure 4. Romi Chassis
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Figure 5. Motor and Encoder Pair



### Microcontroller
[Back to top](#Table-of-Contents)

The STM32 Nucleo-L476RG microcontroller served as the central processing unit for Romi and was provided by the professor. Acting as Romi’s "brain," it processed sensor data, interpreted the readings, and executed control algorithms to drive the motors. This allowed Romi to navigate the course effectively based on real-time feedback. Figure 6 provides a visual representation of the Nucleo board.

<p align="center">
  <img width="300" alt="[Screenshot 2025-03-16 142309" src="https://github.com/user-attachments/assets/ad4143ad-f2fc-4ce5-9881-01eb9068ed2d" />
</p>
<p align="center">
  Figure 6. Nucleo L476RG
</p>

### Sensors
[Back to top](#Table-of-Contents)

Romi utilized three primary sensors: an IMU, a line sensor, and bump sensors. The IMU, which includes an accelerometer, gyroscope, and magnetometer, was used to determine Romi’s heading; however, only the accelerometer and gyroscope were used, as Romi was calibrated at the start of the course to establish a local “north” reference, making the magnetometer unnecessary. The line sensor is a 15-element infrared (IR) sensor array with a 4 mm pitch, though only 10 sensors were used due to the limited number of ADC pins on the Nucleo-L476RG. These sensors produce analog outputs, where higher values correspond to lower reflectivity, allowing Romi to detect the black track lines, which reflected less light. The bump sensors, acting as binary switches, were used to detect the wall near the end of the track, triggering when pressed upon impact. Figures 7-9 illustrate each of these sensors.

<img height="220" alt="[Screenshot 2025-03-16 132044" src="https://github.com/user-attachments/assets/75282655-6f3c-4acc-bebd-a26dc5f86d2b" />
<img height="220" alt="[Screenshot 2025-03-16 124428" src="https://github.com/user-attachments/assets/87a4b780-bd74-4869-acef-98eb18fece45" />
<img height="220" alt="[Screenshot 2025-03-16 132123" src="https://github.com/user-attachments/assets/de5c8547-8330-4591-9034-422a7068c77a" />

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Figure 7. BNO055 IMU
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Figure 8. QTR-HD-15A IR Sensor Array
&nbsp;&nbsp;&nbsp;&nbsp;
Figure 9. Romi Bump Sensor


### Additional Components
[Back to top](#Table-of-Contents)

An HC-05 Bluetooth module was integrated into the system to enable wireless REPL access over Bluetooth. While not essential, this feature provided convenience by eliminating the need for a USB connection between Romi and the computer. To implement this, the HC-05 module was reconfigured with a new name and password, and its baud rate was increased to 460800 for improved communication speed. The HC-05 Bluetooth module used in the project is shown in Figure 10.

<p align="center">
  <img width="350" alt="[Screenshot 2025-03-16 132414" src="https://github.com/user-attachments/assets/7a990adc-fc7c-4450-bb18-58cdf33d645e" />
</p>
<p align="center">
  Figure 10. HC-05 Bluetooth Module
</p>

Standard mounting hardware was used and provided, but any way to mount the various sensors would suffice as long the sensors are mounted according to the manufacturer's specifications.

### Wiring Diagram
[Back to top](#Table-of-Contents)

<p align="center">
  <img width="500" alt="[Screenshot 2025-03-16 153800" src="https://github.com/user-attachments/assets/4b9bbbcd-4be2-4f62-b9b7-f1827ae09b97" />
</p>
<p align="center">
  Figure 11. Wiring Diagram
</p>

## Software
[Back to top](#Table-of-Contents)

### Hardware Drivers

The repository contains the main program file and all necessary hardware driver modules. [main.py](./main.py) is responsible for initializing the hardware and drivers, setting up and executing the scheduler, and managing the finite state machine (FSM). The following driver modules provide hardware interfacing. Further detail is available within each respetive file:

&nbsp;&nbsp;&nbsp;&nbsp;[encoder.py](./encoder.py) – Handles communication with the wheel encoders to measure position and velocity.  

&nbsp;&nbsp;&nbsp;&nbsp;[motor.py](./motor.py) – Controls the Pololu motors for precise actuation.  

&nbsp;&nbsp;&nbsp;&nbsp;[imu.py](./imu.py) – Interfaces with the inertial measurement unit (IMU) for orientation and motion sensing.  

&nbsp;&nbsp;&nbsp;&nbsp;[line.py](./line.py) – Processes input from the line sensors to detect track boundaries. 

&nbsp;&nbsp;&nbsp;&nbsp;[pid.py](./pid.py) – Implements a PID controller for motor speed regulation.

### Task Diagram and FSM
[Back to top](#Table-of-Contents)

Task scheduling and shared variable management are implemented using cotask.py and task_share.py. The task diagram can be seen below in Figure 12. A key limitation on task execution frequency is the resolution of the velocity measurements obtained from the encoders. Through testing, we determined that the maximum feasible task execution rate is approximately 100 Hz. Running all tasks at this frequency did not introduce any performance issues. The scheduler cycles through four tasks:

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

<img height="550" alt="Screenshot 2025-03-14 at 12 37 26 PM" src="https://github.com/user-attachments/assets/b93a4060-abe6-48d0-a5c1-742849eac1dc" />
<img height="550" alt="Screenshot 2025-03-16 at 9 21 26 PM" src="https://github.com/user-attachments/assets/4e732dca-c163-4099-926c-309972505301" />

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Figure 12. Task Diagram
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Figure 13. Finite State Machine

To optimize Romi’s performance, the track was divided into 10 sections, with seven IMU-driven segments dedicated to straight-line motion and three IR sensor-based segments for line following. The corespondng FSM can be seen in Figure 13. Speed adjustments were implemented to enhance efficiency and maneuverability, allowing Romi to travel faster in open, straight sections such as the grid while slowing down in tighter turns to maintain control. This segmentation and adaptive speed control improved overall navigation accuracy and efficiency. A visual representation of the track layout is shown in Figure 14, with notable adjustments for each section summarized in Table 1.

<div align="center">

| Section  | Sensor Used | Modifiers  |
|-----------|-----------|-----------|
| 1    | Line  | velocity = 50% if turn detected  | 
| 2    | IMU  | velocity = 70%  |
| 3    | Line  | velocity = 85%, 70% if harsh turn |
| 4    | Line  | None |
| 5.0  | IMU  | velocity = 150%  |
| 5.1  | IMU  | velocity = 70%   |
| 5.2  | IMU  | velocity = 120%   |
| 5.3  | IMU  | velocity = 120%   |
| 5.4  | IMU  | velocity = 120%   |
| 5.5  | IMU  | None |

</div>

<p align="center">
  Table 1 . Velocity Modifications made in Each Section of FSM
</p>

<p align="center">
  <img height="300" alt="Screenshot 2025-03-16 131934" src="https://github.com/user-attachments/assets/cf0435aa-04fa-48b5-b99e-dcdc10af38d2" />
</p>
<p align="center">
  Figure 14. Course Layout with Denoted Sections
</p>

### Gain Detirmination
[Back to top](#Table-of-Contents)

To account for potential discrepancies between the motors, we conducted a test to determine their individual gains. Each motor was driven at varying effort levels from 0% to 70%, up to the point where the wheels began to slip. The motor gain was then calculated by plotting the steady-state velocity against the applied motor voltage, as shown in Figure 15. A linear fit of the data provided critical insights into both the motor gain and the voltage required to overcome static friction. These values were incorporated into the control system to ensure Romi maintained a nearly perfect straight-line trajectory when no corrective input was applied.

<p align="center">
  <img width="726" alt="Screenshot 2025-02-10 at 9 40 26 PM" src="https://github.com/user-attachments/assets/c75340e4-d59a-4e73-a43b-407469cb99b1" />
</p>
<p align="center">
  Figure 15. Motor Gain
</p>

## Control Theory
[Back to top](#Table-of-Contents)

A feedback control loop was implemented to regulate motor actuation based on real-time sensor data. Romi was assigned an initial longitudinal velocity and yaw rate as setpoints, where the longitudinal velocity controlled Romi’s speed, and the yaw rate was initially set to zero to ensure straight-line motion. Any deviation in yaw rate introduced an error signal, which was used to generate corrective adjustments for turning. The control loop, illustrated in Figure 16, was incorporated into the code to maintain stability and accuracy. Figure 16 was created by Charlie Refvem.

<p align="center">
  <img height="300" alt="Screenshot 2025-03-16 214623" src="https://github.com/user-attachments/assets/303c63f9-43a1-4934-844f-54f5d9f3dde0" />
</p>
<p align="center">
  Figure 16. Control Loop by Charlie Refvem
</p>

## Getting Started
[Back to top](#Table-of-Contents)
  
To use the provided code, first assemble Romi and install the necessary sensors. Ensure all components are wired correctly according to the wiring diagram for proper functionality. For full performance, it is recommended to include the IMU, line sensor, bump sensors, and Bluetooth module. These instructions assume a Windows computer will be used.

To set up via USB, start by powering on Romi using the power button. Connect the microcontroller to the computer with a USB-A to Mini-USB cable, then check the assigned serial port in the Device Manager. Open PuTTY and configure it with the correct serial port and a baud rate of 115200. Transfer all required .py files to PYBFLASH, ensuring the green LED, which indicates file saving, turns off before adding the next file. Once all files are saved, pressing Ctrl+C followed by Ctrl+D in PuTTY will execute main.py.

For Bluetooth setup, save the Bluetooth_Configurator.py file as main.py. Power off Romi, then while holding the button on the HC-05 Bluetooth module, turn Romi back on. The Bluetooth module’s LED should begin blinking slowly, indicating it is in configuration mode. In PuTTY, press Ctrl+C and Ctrl+D to run the script and configure Bluetooth. Identify the serial port assigned to the Bluetooth module, then open a new PuTTY session with a baud rate of 460800. At this point, Bluetooth should be fully operational for wireless communication.


