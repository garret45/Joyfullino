# Joyfullino
A simple two-part solution to accepting an RC receiver input and interpreting as a joystick.

This solution requires no special skills and provides a wireless solution to using a RC remote in simulators.

1.) You connect the PWM outputs of the channels from the RC receiver to pins 2 to 5 on the Arduino.
2.) You upload the Arduino (".ino") sketch to the board and run it using the serial monitor to see:
  - if your pins are connected right and can see the output of wiggling the knobs,
  - the ranges of values that the Arduino is sending back. You will need this for the python script.
3.) Open and edit the python sketch:
  - Match your port (will be the same as the one you used to upload to the bord e.g., COM3 or COM5.
  - Match input the maximum and minimum values that you got for the Serial output of the board.






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
  
