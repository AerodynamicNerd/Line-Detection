# Line-Detection
Using a USB-CAM on a Donkey Car to detect and follow a Line

The code is written in python within the ROS environment on a LINUX platform built on an Nvidia Jetson Nano

steps:

1. clone the usb_cam repository available on github.

2. catkin_make # to build the code in the ROS environment

3. roslaunch the launch file from the repository.

4. run the publisher file # Currently designed to follow yellow lines, detect stop signs and function accordingly but can be manipulated to follow any colored line by changing the range of color.

5. run the subscriber file # Works for donkey cars having I2C protocols.
