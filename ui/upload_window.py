import re
import customtkinter as ctk
from modules.modify_n_upload import modify_n_upload

class Upload_window(ctk.CTkToplevel):
    def __init__(self, parent, data, arduino_file):
        super().__init__(parent)

        self.geometry('400x300')
        self.resizable(False, False)
        self.title('Upload to Arduino')

        self.data = data
        self.arduino_file = arduino_file
        self.fqbn = 'arduino:avr:nano:cpu=atmega328'

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
                                              variable=self.board_var)
        self.board_var.set('Arduino Nano (328)')
        self.board_label.pack(side='left', padx=5)
        self.board_combobox.pack(side='left')

        # com port
        self.com_frame = ctk.CTkFrame(self)
        self.com_label = ctk.CTkLabel(self.com_frame, text='COM port:')
        self.com_entry = ctk.CTkEntry(self.com_frame, textvariable=self.com_var)
        self.com_label.pack(side='left', padx=5)
        self.com_entry.pack(side='left')

        # button
        self.upload_button = ctk.CTkButton(self, text='Upload', command=self.upload)

        self.output = ctk.CTkLabel(self, wraplength=390, textvariable=self.output_var)
        # layout
        self.board_frame.pack(pady=10)
        self.com_frame.pack()
        self.upload_button.pack(pady=10)
        self.output.pack(expand=True, fill='both')

    def update_fqbn(self):
        if(self.board_var == 'Arduino Nano'):
            self.fqbn = 'arduino:avr:nano:cpu=atmega328'
        elif(self.board_var == 'Arduino Nano (old bootloader)'):
            self.fqbn = 'arduino:avr:nano:cpu=atmega328old'
        elif(self.board_var == 'Arduino Uno'):
            self.fqbn = 'arduino:avr:uno'

    def upload(self):
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
        

        self.output_var.set(modify_n_upload(self.arduino_file, self.data, com, self.fqbn))