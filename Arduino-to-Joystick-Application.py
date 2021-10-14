from tkinter import *
import tkinter.messagebox
import threading
import serial  # pip install pySerial
import serial.tools.list_ports as ls
import vgamepad as vg



class Application(Frame, object):
    def __init__(self, master=None, bg_colour='#1565c0', button_colour='#ac0800', textbg_colour='#ffffff', text_colour='#263238', lbl_colour='#ffffff'):
        super(Application, self).__init__(master)
        self.master.config(bg=bg_colour)
        self.joystick_is_running = False

        setup_label = Label(text='Setup', font=("Arial", 15))
        port_label = Label(text='Port :')
        ardu_max_label = Label(text='Arduino max output: ')
        ardu_min_label = Label(text='Arduino min output: ')
        ardu_readl = Label(text='Arduino serial output: ')
        setup_label.config(bg=bg_colour, fg=lbl_colour)
        ardu_readl.config(bg=bg_colour, fg=lbl_colour)
        port_label.config(bg=bg_colour, fg=lbl_colour)
        ardu_max_label.config(bg=bg_colour, fg=lbl_colour)
        ardu_min_label.config(bg=bg_colour, fg=lbl_colour)
        ardu_readl.config(bg=bg_colour, fg=lbl_colour)

        # Ports on windows are COM1 to COM5
        port_list = []
        ports = ls.comports()
        for port, desc, hwid in sorted(ports):
            port_list.append(port)

        # Create Port Dropdown menu
        self.selected_port = StringVar()
        self.selected_port.set(' Port ')
        drop = OptionMenu(root, self.selected_port, *port_list)
        drop.config(bg=button_colour, fg=lbl_colour)

        # make range entry boxes
        self.ardu_max_text = StringVar()
        self.ardu_min_text = StringVar()
        self.ardu_max_text.set('2010')
        self.ardu_min_text.set('975')
        ard_max_textb = Entry(root, width=10, textvariable=self.ardu_max_text)
        ard_min_textb = Entry(root, width=10, textvariable=self.ardu_min_text)
        ard_max_textb.config(bg=textbg_colour, fg=text_colour)
        ard_min_textb.config(bg=textbg_colour, fg=text_colour)

        self.ardu_readln = StringVar()
        ardu_readln = Entry(root, width=25, textvariable=self.ardu_readln, justify='center', font=("Arial", 14), bg=textbg_colour, fg=text_colour) # state=DISABLED,

        # Create button, it will change label text
        start_button = Button(root, width=30, height=4, text=" Start Joystick ", command=self.startJoy, background=button_colour)
        stop_button = Button(root, width=30, height=4, text=" Stop Joystick ", command=self.stopJoy, background=button_colour)
        start_button.config(bg=button_colour, fg=lbl_colour)
        stop_button.config(bg=button_colour, fg=lbl_colour)

        # Set up the grid of labels and other stuff
        setup_label.grid(row=0, column=0, columnspan=2)
        port_label.grid(row=1, column=0)
        ardu_max_label.grid(row=2, column=0)
        ardu_min_label.grid(row=3, column=0)
        ardu_readl.grid(row=4, column=0)

        drop.grid(row=1, column=1)
        ard_max_textb.grid(row=2, column=1)
        ard_min_textb.grid(row=3, column=1)
        ardu_readln.grid(row=5, column=0, columnspan=2, pady=10, padx=15)
        start_button.grid(row=6, column=0, columnspan=2, pady=10, padx=15)
        stop_button.grid(row=7, column=0, columnspan=2, pady=10, padx=15)


    def startJoy(self):
        if not self.joystick_is_running:
            # open serial port
            port = self.selected_port.get()
            if port in [' Port ', '']:
                tkinter.messagebox.showwarning('Port Open Fail',
                                               'Port open fail. Please select a port')
                return
            try:
                self.ser = serial.Serial(port, 19200, timeout=2)
                if not self.ser.isOpen():
                    self.ser.open()
            except OSError:
                tkinter.messagebox.showwarning('Port Open Fail',
                                               'Port open fail. Try checking the port in Arduino IDE tools>Ports')
                return

            self.max_arduino = int(self.ardu_max_text.get())
            self.min_arduino = int(self.ardu_min_text.get())

            self.gamepad = vg.VX360Gamepad()
            self.max_joy = 32767
            # min_joy = -32768

            self.mid_arduino = (self.max_arduino + self.min_arduino) / 2
            self.rng_arduino = self.max_arduino - self.min_arduino

            self.rescale = 2 * self.max_joy / self.rng_arduino

            self.joystick_is_running = True
            self.joystick_thread = threading.Thread(target=self.joystick).start()


    def stopJoy(self):
        self.joystick_is_running = False
        self.ser.close()


    def domain(self, val):
        max = self.max_joy
        if val > max:
            return max
        elif val < -max:
            return -max
        else:
            return val


    def joystick(self):
        # to send to Arduino: try:
        # stuff = 'some words'
        # ser.write(stuff.encode()
        # ser.write(stuff.encode())
        count = 0
        while self.joystick_is_running:
            count += 1
            cha = [0, 0, 0, 0]
            try:
                # in case the readline() started half way through a println() in the arduino
                line = self.ser.readline().decode('utf-8')
                if len(line.split()) >= 4:
                    # get each Arduino readout, subtract lowwer threshhold and rescale as in interger in the vgamepad domain [ +32767, -32767 ]
                    cha = [self.domain( int((float(j) - self.mid_arduino) * self.rescale)) for j in line.split()]
                    if count > 10:
                        count = 0
                        self.ardu_readln.set(line)
            except UnicodeDecodeError:
                pass
            except KeyboardInterrupt:
                pass
            except TypeError:
                pass

            self.gamepad.left_joystick(x_value=cha[0], y_value=cha[1])  # values between -32768 and 32767
            self.gamepad.right_joystick(x_value=cha[2], y_value=cha[3])  # values between -32768 and 32767
            self.gamepad.update()


if __name__ == '__main__':
    # Create object
    root = Tk()
    app = Application()
    app.master.title('Joyfullino')
    app.mainloop()