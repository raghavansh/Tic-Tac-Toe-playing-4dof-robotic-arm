# Tic-Tac-Toe-playing-4dof-robotic-arm
Designed and built a 4 dof robotic arm that can move its head to any given coordinate, and play against human, programmed using inverse kinematics and mini max algorithm.
## Introduction:
We successfully made a 4-dof robotic arm play a tic tac toe game by coding in python and communicating the instruction to Arduino using pyfirmata library.
The arm is capable of playing tic-tac-toe against human. It determines the move made by human and accordingly makes its best moves.
We made the hardware part of the bot by referring to given tutorial videos. Inverse kinematics function has been applied in code for the robot to move in a particular coordinate in cylindrical coordinate system. To play the game, the phone camera has been used to identify the coins colours and moves using openCV library. When the user places a green coin, according to the code it places the red coin in the way the bot can win.
## Video showing the robot in action
https://user-images.githubusercontent.com/78599181/176186775-ac6979bf-f293-4861-82ca-bb21442997b3.mov
## Requirements:
* 4dof Robotic arm (you may 3d print,or buy the parts and then assemble it.)
* Following python libraries:
pyfirmata,cv2,numpy,imutils,sympy
* Arduino
* Servos
* Mobile
* laptop
* white paper and coloured blocks for tic-tac-toe game.

## Steps:
* first load the standard firmata code on arudino using arudino ide.
* Identify the port being used by your arudnio board from arduino ide.
* now everything is ready to communicate with arudino using python
* run code.py
* make sure the baud rate of aruduino and the serial port number is same as that in the python code and you are good to go.
* to capture live video, you can use any video sharing app that lets you to share the camera video from your mobile to PC over wifi.
* place the camera over the setup so that it can detect every changes in the playing board.





