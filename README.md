# ME-405-Mecha16 Term Project
### Wyatt Eberhart and Ethan Gray

## Table of Contents
- [Project Overview](#projectoverview)
- [Hardware](#hardware)
- [Sensors](#sensors)

### Project Overview
- [Back to top](#Table-of-Contents)

This repository contains the ME-405 term project by Ethan Gray and Wyatt Eberhart. The objective of this project was to develop and implement a control system for a differential-drive robot, Romi, using MicroPython. Romi was programmed to autonomously navigate a predefined course (depicted in Figure 1) by utilizing three primary sensors: an inertial measurement unit (IMU), line sensors, and bump sensors. These sensors were integrated with the Romi chassis kit and combined with Pololu motors and a Pololu power distribution board.

The system was controlled using an STM32 Nucleo-L476RG development board, which served as the main processing unit. Task execution was managed through a real-time scheduler, ensuring periodic execution with designated priorities. Within these scheduled tasks, a finite state machine (FSM) was implemented to enable Romi to know what section of the track it was on and react accordingly.

<img width="1389" alt="Screenshot 2025-03-16 at 12 55 04 PM" src="https://github.com/user-attachments/assets/97ac74ea-d0b5-4674-859b-4bc7075b9cf2" />
<p align="center">
  Figure 1. Course Layout
</p>





![Screenshot 2025-03-16 121312](https://github.com/user-attachments/assets/e07e3801-c6db-4c03-9c3a-d3de6e2d6846)

<p align="center">
  Figure 1. Wiring Diagram
</p>

https://youtube.com/shorts/zJc4XDnnLkc

### Hardware
- [Back to top](#Table-of-Contents)

### Sensors
- [Back to top](#Table-of-Contents)
