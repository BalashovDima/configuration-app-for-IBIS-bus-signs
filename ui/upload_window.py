import re
import threading
import time
import customtkinter as ctk
from modules.modify_n_upload import modify_n_upload
from modules.is_arduino_library_installed import check_arduino_library

class Upload_window(ctk.CTkToplevel):
    def __init__(self, parent, data, arduino_file):
        super().__init__(parent)

        self.geometry('520x370')
        self.resizable(False, False)
        self.title('Upload to Arduino')

        self.data = data
        self.arduino_file = arduino_file
        self.fqbn = 'arduino:avr:nano:cpu=atmega328'

        self.lib_list = {'LiquidCrystal': '1.0.7', 
                         'RTClib': '2.1.1', 
                         'Adafruit BusIO': '1.14.1', 
                         'Wire': '1.0', 
                         'AnalogKey': '1.1', 
                         'EncButton': '2.0', 
                         'EEPROM': '2.0', 
                         'SPI': '1.0',
                         }

        # variables
        self.board_var = ctk.StringVar()
        self.com_var = ctk.StringVar(value='COM')
        self.output_var = ctk.StringVar(value=' ')

        # board
        self.board_frame = ctk.CTkFrame(self)
        self.board_label = ctk.CTkLabel(self.board_frame, text='Select board:')
        self.board_combobox = ctk.CTkComboBox(self.board_frame, 
                                              values=['Arduino Nano (328)', 
                                                      'Arduino Nano (328 old bootloader)', 
                                                      'Arduino Uno'], 
                                              variable=self.board_var,
                                              width=200)
        self.board_var.set('Arduino Nano (328)')
        self.board_label.pack(side='left', padx=5)
        self.board_combobox.pack(side='left')

        # event handling
        self.board_var.trace_add("write", self.update_fqbn)

        # com port
        self.com_frame = ctk.CTkFrame(self)
        self.com_label = ctk.CTkLabel(self.com_frame, text='COM port:')
        self.com_entry = ctk.CTkEntry(self.com_frame, textvariable=self.com_var)
        self.com_label.pack(side='left', padx=5)
        self.com_entry.pack(side='left')

        # button
        self.upload_button = ctk.CTkButton(self, text='Upload', command=self.upload)

        # output
        self.output = ctk.CTkTextbox(self)
        # in progress indicator
        self.inprogress_var = ctk.StringVar(value='')
        self.inprogress_label = ctk.CTkLabel(self, textvariable = self.inprogress_var, font=('Calibri', 20))
        self.inprogress_label.place(x=10, y=5)

        # layout
        self.board_frame.pack(pady=10)
        self.com_frame.pack()
        self.upload_button.pack(pady=10)
        self.output.pack(expand=True, fill='both')

    def update_fqbn(self, *args):
        if(self.board_var.get() == 'Arduino Nano (328)'):
            self.fqbn = 'arduino:avr:nano:cpu=atmega328'
        elif(self.board_var.get() == 'Arduino Nano (328 old bootloader)'):
            self.fqbn = 'arduino:avr:nano:cpu=atmega328old'
        elif(self.board_var.get() == 'Arduino Uno'):
            self.fqbn = 'arduino:avr:uno'

    def upload(self):
        #get com port number using regular expression
        pattern = re.compile(r'^com(\d)$', re.IGNORECASE)
        match = pattern.match(self.com_var.get())

        com = None
        if match:
            number = match.group(1)
            com = f'COM{number.upper()}'
        elif self.com_var.get().isdigit():
            com = f'COM{com}'
        else:
            self.output_var.set('Invalid COM port')
            return
        
        self.output.delete(0.0, ctk.END)
        self.upload_button.configure(state="disabled")

        # check libraries
        thread = threading.Thread(target=lambda: setattr(thread, 'result', check_arduino_library(self.lib_list)))
        thread.start()
        counter = 0
        while not hasattr(thread, 'result'):
            print(".", end="", flush=True)
            text = ''
            if counter == 0:
                text = '⦿'
            elif counter == 1:
                text = '⦿⦿'
            elif counter == 2:
                text = '⦿⦿⦿'
            counter = (counter + 1) % 3
            self.inprogress_var.set(text)
            self.update()
            time.sleep(0.3)
        self.inprogress_var.set('')
        thread.join()
        stop_upload = False
        for lib in thread.result:
            if not lib.installed:
                self.output.insert(ctk.END, f'ERROR: Library \'{lib.name}\' is not installed, cannot compile.\n')
                stop_upload = True
            elif lib.version != self.lib_list[lib.name]:
                self.output.insert(ctk.END, f'WARNING: \'{lib.name}\' version is recommended to be @{self.lib_list[lib.name]} (currently it is @{lib.version}). Sketch might not compile if the version are not compatible\n')
                stop_upload = True

        if stop_upload: 
            self.upload_button.configure(state="enabled")
            return

        # upload and save the output, then show the output
        uploading_output = modify_n_upload(file_path=self.arduino_file, data=self.data, com=com, fqbn=self.fqbn, inprogress_label_var = self.inprogress_var, window=self)
        self.output.insert(ctk.END, ''.join(uploading_output))

        self.upload_button.configure(state="enabled")