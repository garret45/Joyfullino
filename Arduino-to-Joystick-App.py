import tkinter.messagebox
import serial
import serial.tools.list_ports as ls
import vgamepad as vg
from tkinter import *


class Application(Frame, object):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        # add event scheduler so buttons and joystick loop work
        self.after_id = None
        self.secs = 0
        self.init_joy = False

        # Ports on windows are COM1 to COM5
        port_list = []
        ports = ls.comports()
        for port, desc, hwid in sorted(ports):
            port_list.append(port)

        # Create Dropdown menu
        self.selected_port = StringVar()
        self.selected_port.set(' Port ')
        drop = OptionMenu(root, self.selected_port, *port_list).grid(row=0, column=0, columnspan=2)

        ardu_max_label = Label(text='Arduino Max Output: ').grid(row=1, column=0)
        ardu_min_label = Label(text='Arduino Min Output: ').grid(row=2, column=0)
        ardu_readl = Label(text='Arduino Output: ').grid(row=3, column=0)

        self.ardu_max_text = StringVar()
        self.ardu_min_text = StringVar()
        self.ardu_max_text.set('2000')
        self.ardu_min_text.set('1000')
        ard_max_textb = Entry(root, width = 10, textvariable = self.ardu_max_text).grid(row=1, column=1)
        ard_min_textb = Entry(root, width = 10, textvariable = self.ardu_min_text).grid(row=2, column=1)

        self.ardu_readln = StringVar()
        ardu_readln = Entry(root, width = 50, textvariable = self.ardu_readln, state=DISABLED).grid(row=4, column=0, columnspan=2)

        # Create button, it will change label text
        start_button = Button(root, width=30, text=" Start Joystick ", command=self.startJoy).grid(row=5, column=0, columnspan=2)
        stop_button = Button(root, width=30, text=" Stop Joystick ", command=self.stopJoy).grid(row=6, column=0, columnspan=2)


    def startJoy(self):
        if not self.init_joy:
            self.initJoy()
        if self.init_joy:
            self.joystick()

    def stopJoy(self):
        if self.after_id:
            root.after_cancel(self.after_id)
            self.after_id = None
        self.gamepad.__del__()
        self.ser.close()
        self.init_joy = False

    def initJoy(self):

        # open serial port
        port = self.selected_port.get()
        if port == ' Port ':
            tkinter.messagebox.showwarning('Port Open Fail',
                                           'Port open fail. Please select a port')
            return
        try:
            self.ser = serial.Serial(port, 19200, timeout=2)
        except OSError:
            tkinter.messagebox.showwarning('Port Open Fail', 'Port open fail. Try checking the port in Arduino IDE tools>Ports')
            return
        if not self.ser.isOpen():
            self.ser.open()

        self.max_arduino = int(self.ardu_max_text.get())
        self.min_arduino = int(self.ardu_min_text.get())

        self.gamepad = vg.VX360Gamepad()
        self.max_joy = 32767
        min_joy = -32768

        self.mid_arduino = (self.max_arduino + self.min_arduino)/2
        self.rng_arduino = self.max_arduino - self.min_arduino

        self.rescale = 2 * self.max_joy / self.rng_arduino

        # only need to do this once: startJoy() checks this
        self.init_joy = True


    def joystick(self):
        # to send to Arduino: try:
        # stuff = 'some words'
        # ser.write(stuff.encode()
        # ser.write(stuff.encode())
        for i in range(0, 50):
            cha = [0, 0, 0, 0]
            try:
                # in case the readline() started half way through a println() in the arduino
                line = self.ser.readline().decode('utf-8')
                if len(line.split()) >= 4:
                    cha = [int((float(j) - self.mid_arduino) * self.rescale) for j in line.split()]
                    print(cha, line)
            except UnicodeDecodeError:
                pass
            except KeyboardInterrupt:
                pass

            self.gamepad.left_joystick(x_value=cha[0], y_value=cha[1])  # values between -32768 and 32767
            self.gamepad.right_joystick(x_value=cha[2], y_value=cha[3])  # values between -32768 and 32767
            self.gamepad.update()

        self.ardu_readln.set(line)
        self.after_id = root.after(60, self.joystick)


if __name__ == '__main__':
    # Create object
    root = Tk()
    app = Application()
    app.master.title('Joyfullino')
    app.master.geometry('300x200')
    app.master.config(bg='#fafafa')
    app.mainloop()