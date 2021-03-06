# Rover
This is the code for my Rover that I built myself at home. The robot has 4 primary components:

- Arm
- 2 wheeled base
- Camera
- and a website that is used to control it.

## Dependencies 
Python libraries required to run this:
- OpenCV
- Flask
- Numpy
- Adafruit Servokit
- PySerial

## Usage
Make sure everything is connected properly. The Raspberry Pi to the arduino, the PCA9685 and the camera. The PCA9685 to the servos and the arduino to the motors. Clone this repo using git clone, say your prayers and run the following:

<code> sudo python3 main.py </code>

## The Rover (technical details)

The way this whole thing is configured is that the Raspberry Pi is the main brains of the system. To it there are a few sub-brains(?) that allow the appropriate transfer of data or signals. These sub-brains are the arduino and the PCA9685, which controls the base and the arm respectively. The Raspberry Pi sends data to the arduino via serial communication using a library called PySerial and the it also sends data to the PCA9685 by using I2C communication via a library called adafruit_servokit. To the camera not only is data recieved but data about the cursor location on the camera feed is also sent. The data received is of the camera video feed which is displayed on the website. 

### The Arm
The arm is controlled from the rover website. There are two pages from which you can control the arm from. The inverse kinematic page allows user to get coordinates from a video feed and the user can later input those coordinates into the x, y and z box and the arm will move to the positon they set. The forward kinematic page allows user to manually set the the angle at which each servo in the arm should rotate. 

For more information about the arm you can check [here](https://github.com/Vulcan758/InverseKinematicsPi)

### The Base

The base is controlled by an arduino that has a motor shield attached to it but the same can be done with a L298 motor driver module. The arduino code is such that the wheels rotate for a split second each time "w", "a", "s" or "d" is entered into the arduino serial terminal. 

Later on I have a script made in the roverLibs directory called roverBase. Here using pyserial the script sends over the keys to the serial terminal directly after it receives the key values from the user. The user can send key press values when they enter the website and control the robot from the website completely.

### The Camera 

The rover uses a RaspiCam, you can probably use a regular webcam laying around at home as well but if you dont have one, these work great and are less expensive. The camera video feed is streamed into the website and in the inverse kinematics page you will see that the feed had a white cursor type thing. You can control this using the arrow keys and when you click enter, you will get the real world coordinates returned which you can enter into the xyz box. 

These real world coordinates come as a result of image mapping and some mathematical equations using the image mapping data I captured and collected. 

### The Website

This website here is generated off of a web server from the Raspberry Pi. Like all websites there are two main components here: the backend and the frontend. The backend is made using Flask, a Python micro web framework and the frontend is made with a combination of Javascript, HTML and CSS.

Siding away from tradition, due to the lack of neccessity and my lack of patience for completing this project the frontend here is less about design and UI and more about sending data from one system to another. 

Before continuing, allow me to explain the architecture of the whole system. The client (the main web page) sends data (i.e. key board presses, coordinates, angles, etc) to the server (the Raspberry Pi), the server then sends this data to the main robot controllers (also the Raspberry Pi, which sends data to the motor drivers via I2C and serial) and at the same time, the main robot sends data (video feed, coordinates, etc) to the server and the server sends this to the client which allows the user to see different things like the video feed.

Here I primarily used Javascript send key press events for the cursor or for controlling the rover base and this key press data is sent to the backend server on the Raspberry Pi which translates the data a little bit and sends them over to the robot hence allowing the robot to move around. 

All of this sounds like a lot but the latency isnt as much as you would expect and is much better than compared to running this whole system on a GUI application on the Raspberry Pi as opposed to a web interface as shown here.

Hope everyone who comes across this likes it, its a massive passion project and something I'm really really proud of. Thank you <3.


- Al Mahir Ahmed (Vulcan)
