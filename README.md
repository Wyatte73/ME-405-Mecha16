# ME-405-Mecha16 Term Project
### Ethan Gray and Wyatt Eberhart

## Table of Contents
- [Project Overview](#projectoverview)
- [Hardware](#hardware)
- [Sensors](#sensors)

## Project Overview
- [Back to top](#Table-of-Contents)

This repository contains the ME-405 term project by Ethan Gray and Wyatt Eberhart. The objective of this project was to develop and implement a control system for a differential-drive robot, Romi, using MicroPython. Romi was programmed to autonomously navigate a predefined course (depicted in Figure 1) by utilizing three primary sensors: an inertial measurement unit (IMU), line sensors, and bump sensors. These sensors were integrated with the Romi chassis kit and combined with Pololu motors and a Pololu power distribution board.

The system was controlled using an STM32 Nucleo-L476RG development board, which served as the main processing unit. Task execution was managed through a real-time scheduler, ensuring periodic execution with designated priorities. Within these scheduled tasks, a finite state machine (FSM) was implemented to enable Romi to know what section of the track it was on and react accordingly.

<img width="1389" alt="Screenshot 2025-03-16 at 12 55 04 PM" src="https://github.com/user-attachments/assets/97ac74ea-d0b5-4674-859b-4bc7075b9cf2" />
<p align="center">
  Figure 1. Course Layout
</p>

https://youtube.com/shorts/zJc4XDnnLkc

### Hardware
- [Back to top](#Table-of-Contents)

## Software
- [Back to top](#Table-of-Contents)

The repository contains the main program file and all necessary hardware driver modules. main.py is responsible for initializing the hardware and drivers, setting up and executing the scheduler, and managing the finite state machine (FSM). The following driver modules provide hardware interfacing:

&nbsp;&nbsp;&nbsp;&nbsp;encoder.py – Handles communication with the wheel encoders to measure position and velocity.  

&nbsp;&nbsp;&nbsp;&nbsp;motor.py – Controls the Pololu motors for precise actuation.  

&nbsp;&nbsp;&nbsp;&nbsp;imu.py – Interfaces with the inertial measurement unit (IMU) for orientation and motion sensing.  

&nbsp;&nbsp;&nbsp;&nbsp;line.py – Processes input from the line sensors to detect track boundaries. 

&nbsp;&nbsp;&nbsp;&nbsp;pid.py – Implements a PID controller for motor speed regulation.
  
Task scheduling and shared variable management are implemented using cotask.py and task_share.py. A key limitation on task execution frequency is the resolution of the velocity measurements obtained from the encoders. Through testing, we determined that the maximum feasible task execution rate is approximately 100 Hz. Running all tasks at this frequency did not introduce any performance issues. The scheduler cycles through four tasks:

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


### Sensors
- [Back to top](#Table-of-Contents)
