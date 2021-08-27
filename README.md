# Rover
This is the code for my Rover that I built myself at home. The robot has 4 primary components:

- Arm
- 2 wheeled base
- Camera
- and a website that is used to control it.

## The Arm
The arm is controlled from the rover website. There are two pages from which you can control the arm from. The inverse kinematic page allows user to get coordinates from a video feed and the user can later input those coordinates into the x, y and z box and the arm will move to the positon they set. The forward kinematic page allows user to manually set the the angle at which each servo in the arm should rotate. 

For more information about the arm you can check [here](https://github.com/Vulcan758/InverseKinematicsPi)

## The Base

The base is controlled by an arduino that has a motor shield attached to it but the same can be done with a L298 motor driver module. The arduino code is such that the wheels rotate for a split second each time "w", "a", "s" or "d" is entered into the arduino serial terminal. 

Later on I have a script made in the roverLibs directory called roverBase. Here using pyserial the script sends over the keys to the serial terminal directly after it receives the key values from the user. The user can send key press values when they enter the website and control the robot from the website completely.

## The Camera 

The rover uses a RaspiCam, you can probably use a regular webcam laying around at home as well but if you dont have one, these work great and are less expensive. The camera video feed is streamed into the website and in the inverse kinematics page you will see that the feed had a white cursor type thing. You can control this using the arrow keys and when you click enter, you will get the real world coordinates returned which you can enter into the xyz box. 

These real world coordinates come as a result of image mapping and some mathematical equations using the image mapping data I captured and collected. 

## The Website

This website here is generated off of a web server from the Raspberry Pi. Like all websites there are two main components here: the backend and the frontend. The backend is made using Flask, a Python micro web framework and the frontend is made with a combination of Javascript, HTML and CSS.

Siding away from tradition, due to the lack of neccessity and my lack of patience for completing this project the frontend here is less about design and UI and more about sending data from one system to another. 

Before continuing, allow me to explain the architecture of the whole system. The client (the main web page) sends data (i.e. key board presses, coordinates, angles, etc) to the server (the Raspberry Pi), the server then sends this data to the main robot controllers (also the Raspberry Pi, which sends data to the motor drivers via I2C and serial) and at the same time, the main robot sends data (video feed, coordinates, etc) to the server and the server sends this to the client which allows the user to see different things like the video feed.

Here I primarily used Javascript send key press events to the 
