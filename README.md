# Joyfullino
A simple two-part solution to accepting an RC receiver input and interpreting as a joystick.

This solution requires no special skills and provides a wireless solution to using a RC remote in simulators.

To run:
* Install and open the Arduino IDE:  https://www.arduino.cc/en/software
* Plug in the Arduino
* In the Arduino IDE open the file: "PWM_Serial_Output.ino"
* Select the sideways arrow to upload the file. If this fails change the port in Tools>Port. Remember what port works.
* Connect the Receiver to the 5v and ground (GND) and the channels to pins 2, 3, 4 and 5 (the order is usually not important)
* Open the serial monitor to check that you are getting outputs that move with each stick axis. Close when done (important!)
* Install Python:  https://www.python.org/downloads/
* Open the windows command line and past:  pip install pySerial, vgamepad
* Install the drivers that pop up
* Run the python file "Arduino-to-Joystick-App.py" by right-clicking>Open With>Python



This may not be the best solution for you and if you are in a similar boat to me than helpful resources are:
  
  The Python joystick library
    https://pypi.org/project/vgamepad/#getting-started
  
  How to get the PWM of a RC receiver:
    https://youtu.be/u0Ft8SB3pkw
  
  How to read the serial output of an Arduino in Python:
    https://stackoverflow.com/questions/2291772/virtual-serial-device-in-python
    
  
  
  Other Methods of achieving the same thing (that were not applicable to me but may save you time):
    
   Use the drone flight-board as a wireless receiver and joystick:
    https://oscarliang.com/betaflight-fc-fpv-simulator/
      
   Connect the RC receiver to an Arduino and run that as a joystick (requires the receiver to have PPM and needs a very specific Arduino):
    https://youtu.be/cZc-23NjNHY
  
