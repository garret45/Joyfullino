import serial
import vgamepad as vg

# Ports on windows are COM1 to COM5
port = 'COM3'
max_arduino = 2000
min_arduino = 1000

# open serial port
ser = serial.Serial( port, 19200, timeout=2)
if not ser.isOpen():
    ser.open()

mid_arduino = (max_arduino + min_arduino)/2
rng_arduino = max_arduino - min_arduino

gamepad = vg.VX360Gamepad()
max_joy = 32767
min_joy = -32768

# to write: try:
# stuff = 'some words'
#ser.write(stuff.encode())
cha = [0, 0, 0, 0]
while True:
    #ser.write(stuff.encode())
    try:
        line = ser.readline().decode('utf-8')
        cha = [int((float(j) - mid_arduino) * 2 * max_joy / rng_arduino) for j in line.split()]
        print(cha, line)
    except UnicodeDecodeError:
        pass
    except KeyboardInterrupt:
        pass

    gamepad.left_joystick(x_value=cha[0], y_value=cha[1])  # values between -32768 and 32767
    gamepad.right_joystick(x_value=cha[2], y_value=cha[3])  # values between -32768 and 32767
    gamepad.update()



