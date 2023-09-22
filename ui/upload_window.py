import re
import threading
from threading import Timer
import datetime
import subprocess
import customtkinter as ctk
from modules.modify_n_upload import modify_n_upload
from modules.is_arduino_library_installed import check_arduino_library
from ui.install_missing_components_window import Install_missing_components_window

class Upload_window(ctk.CTkToplevel):
    def __init__(self, parent, data, arduino_file):
        super().__init__(parent)

        self.geometry('520x370')
        self.resizable(False, False)
        self.title('Upload to Arduino')

        self.data = data
        self.arduino_file = arduino_file
        self.fqbn = 'arduino:avr:nano:cpu=atmega328'
        self.com = ''
        self.loading_animetion_prevtime = datetime.datetime.now()
        self.loading_count = 1

        self.lib_list = {'LiquidCrystal': '1.0.7', 
                         'RTClib': '2.1.1', 
                         'AnalogKey': '1.1', 
                         'EncButton': '2.0', 
                        # libraries below are installed automatically (adafruit busio with rtclib, other three are a part of arduino:avr core)
                         'Adafruit BusIO': '1.14.1', 
                         'Wire': '1.0', 
                         'EEPROM': '2.0', 
                         'SPI': '1.0',
                         }

        # variables
        self.board_var = ctk.StringVar()
        self.com_var = ctk.StringVar(value='')

        # board
        self.board_frame = ctk.CTkFrame(self)
        self.board_label = ctk.CTkLabel(self.board_frame, text='Select board:')
        self.board_combobox = ctk.CTkComboBox(self.board_frame, 
                                              values=['Arduino Nano (328)', 
                                                      'Arduino Nano (328 old bootloader)', 
                                                      'Arduino Uno'], 
                                              variable=self.board_var,
                                              width=200,
                                              state='readonly')
        self.board_var.set('Arduino Nano (328)')
        self.board_label.pack(side='left', padx=5)
        self.board_combobox.pack(side='left')

        # event handling
        self.board_var.trace_add("write", self.update_fqbn)

        # com port
        self.com_frame = ctk.CTkFrame(self)
        self.com_label = ctk.CTkLabel(self.com_frame, text='COM port:')
        self.com_combobox = ctk.CTkComboBox(self.com_frame, variable=self.com_var, values=(''))
        self.reload_connected_boards_button = ctk.CTkButton(self.com_frame, text='⟳', font=('Calibri', 20), command=self.load_boards, width=15)
        self.com_label.pack(side='left', padx=5)
        self.com_combobox.pack(side='left')
        self.reload_connected_boards_button.pack(side='left', padx=(5,0))

        # button
        self.upload_button = ctk.CTkButton(self, text='Upload', command=self.upload, state='disabled')

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

        self.install_missing_components_window = None
        self.install_missing_components_button = ctk.CTkButton(self, text='Install missing components', command=self.install_missing_components)
        Timer(0.3, lambda:self.launch_prerequisites_check()).start()

    def launch_prerequisites_check(self):
        thread = threading.Thread(target=lambda: setattr(thread, 'missing_components', self.prerequisites_check()))
        thread.start()
        while not hasattr(thread, 'missing_components'): # display animetion while prerequisites are being checked
            self.loading_animetion()
        self.inprogress_var.set('')
        thread.join()

        if thread.missing_components:
            self.missing_components = thread.missing_components

            x_coordinate = self.winfo_width() - 10 - self.install_missing_components_button.winfo_reqwidth()
            y_coordinate = self.winfo_height() - 10 - self.install_missing_components_button.winfo_reqheight()

            self.install_missing_components_button.place(x=x_coordinate, y=y_coordinate)

            # allow upload if the only thing missing is a library (or libraries) of wrong version
            if not self.missing_components['cli'] and not self.missing_components['avr-core'] and not len(self.missing_components['libs']):
                self.upload_button.configure(state='normal')
            return

        # add com numbers of connected boards
        self.load_boards()
        self.upload_button.configure(state='normal')

    def prerequisites_check(self):
        self.output.delete(0.0, ctk.END)
        missing_components = {'cli': False, 'avr-core': False, 'libs': [], 'wrong-version-libs': []}
        # check if arduino-cli is installed
        if self.is_arduino_cli_installed():
            self.output.insert(ctk.END, "✔ Arduino cli is installed ✔\n")
        else:
            self.output.insert(ctk.END, "✖ Arduino cli is NOT installed ✖\n")
            missing_components['cli'] = True
            return missing_components
        
        # check if avr core is installed
        if self.is_arduino_avr_core_installed():
            self.output.insert(ctk.END, "✔ Arduino AVR core is installed ✔\n")
        else:
            self.output.insert(ctk.END, "✖ Arduino AVR core is NOT installed ✖\n")
            missing_components['avr-core'] = True

        # check if all the libraries are installed
        libs_check_results = check_arduino_library(self.lib_list)
        libs_installed = True
        for lib in libs_check_results:
            if not lib.installed:
                self.output.insert(ctk.END, f'✖ Library \'{lib.name}\' is not installed ✖\n')
                libs_installed = False
                missing_components['libs'].append({'name': lib.name, 'version': self.lib_list[lib.name]})
            elif lib.version != self.lib_list[lib.name]:
                self.output.insert(ctk.END, f'warning: \'{lib.name}\' version is recommended to be @{self.lib_list[lib.name]} (currently it is @{lib.version}). Sketch might not compile if the versions are not compatible\n')
                missing_components['wrong-version-libs'].append({'name': lib.name, 'version': self.lib_list[lib.name]})
        if libs_installed:
            self.output.insert(ctk.END, "✔ All needed arduino libraries are installed ✔\n")
            
        if(missing_components['cli'] 
           or missing_components['avr-core']
           or len(missing_components['libs'])
           or len(missing_components['wrong-version-libs'])): 
            return missing_components
        
        return False
    
    def install_missing_components(self):
        if self.install_missing_components_window is None or not self.install_missing_components_window.winfo_exists():
            self.install_missing_components_window = Install_missing_components_window(self, self.missing_components) # create window if its None or destroyed
        # for ui rendering test ↓↓↓↓↓
            # self.install_missing_components_window = Install_missing_components_window(self, {'cli': True, 
            #               'avr-core': True, 
            #               'libs': [
            #                   {'name': 'some-library', 'version': '1.2.3'},
            #                   {'name': 'test-not-existent', 'version': '3.4.1'},
            #                   {'name': 'don\'t-know', 'version': '3.4.1'},
            #                   {'name': 'another', 'version': '1.1.1'}
            #                   ], 
            #               'wrong-version-libs': [
            #                   {'name': 'wrong-version-library', 'version': '12.3.1'},
            #                   {'name': 'EncButton', 'version': '3.1.0'},
            #                   {'name': 'something', 'version': '2.3.1'}
            #                   ]}) 
        # for ui rendering test ^^^^^

            self.install_missing_components_window.protocol("WM_DELETE_WINDOW", self.close_inst_mis_comp_window)
            self.install_missing_components_window.done_button.bind('<Button-1>', self.close_inst_mis_comp_window)
            Timer(0.3, lambda:self.install_missing_components_window.focus()).start()
        else:
            self.install_missing_components_window.focus()  # if window exists focus it

    def close_inst_mis_comp_window(self, event=None):
        self.install_missing_components_window.destroy()
        self.install_missing_components_button.place_forget()
        self.launch_prerequisites_check()

    def is_arduino_cli_installed(self):
        process = subprocess.Popen(["arduino-cli"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return False
    
        # Check if the output contains version information (or other indicators of success)
        if b"Arduino CLI" in stdout:
            return True
        else:
            return False
        
    def is_arduino_avr_core_installed(self):
        try:
            process = subprocess.Popen(["arduino-cli", "core", "list"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            if "arduino:avr" in stdout:
                return True
            else:
                return False
        except FileNotFoundError:
            return False

    def update_fqbn(self, *args):
        if(self.board_var.get() == 'Arduino Nano (328)'):
            self.fqbn = 'arduino:avr:nano:cpu=atmega328'
        elif(self.board_var.get() == 'Arduino Nano (328 old bootloader)'):
            self.fqbn = 'arduino:avr:nano:cpu=atmega328old'
        elif(self.board_var.get() == 'Arduino Uno'):
            self.fqbn = 'arduino:avr:uno'

    def get_connected_arduino_boards(self):
        try:
            # Run the arduino-cli board list command
            process = subprocess.Popen(["arduino-cli", "board", "list"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            process.wait()  # Wait for the process to finish

            # Parse the output to extract the board information
            board_list = []
            lines = stdout.splitlines()
            for line in lines[1:]:  # Skip the header line
                parts = line.split()
                if len(parts) >= 3:
                    port = parts[0]
                    board_list.append(port)

            return board_list
        except FileNotFoundError:
            return []
    
    def load_boards(self):
        self.output.insert(ctk.END, "Looking for connected boards...")

        boards_thread = threading.Thread(target=lambda: setattr(boards_thread, 'result', self.get_connected_arduino_boards()))
        boards_thread.start()

        while not hasattr(boards_thread, 'result'):
            self.loading_animetion()
        self.inprogress_var.set('')
        
        boards_thread.join()

        self.com_combobox.configure(values=boards_thread.result)
        if len(boards_thread.result):
            self.com_var.set(boards_thread.result[0])
        else:
            self.com_var.set('')

        # remove 'Looking for connected boards...' from output textbox
        last_char_position = self.output.index("end-1c")
        last_line_start = self.output.index(f"{last_char_position} linestart")
        self.output.delete(last_line_start, last_char_position)

    def com_check(self, com):
        '''Checks whether 'com' is valid

        Argument: 'com' -- string to check.
        Returns: False if 'com' is not valid, else string in format 'COM<number>'
        '''
        if com.isdigit():
            if int(com) > 19: return False
            return f'COM{com}'
        
        # get com port number using regular expression
        pattern = re.compile(r'^com(\d\d?)$', re.IGNORECASE)
        match = pattern.match(com)

        if match:
            number = match.group(1)
            if int(number) > 19: return False
            return f'COM{number}'
        
        return False

    def upload(self):
        com = self.com_check(self.com_var.get())
        if not com:
            self.output.insert(ctk.END, 'Invalid COM port')
            return

        self.output.delete(0.0, ctk.END)
        self.upload_button.configure(state="disabled")

        # upload and save the output, then show the output
        uploading_output = modify_n_upload(file_path=self.arduino_file, data=self.data, com=com, fqbn=self.fqbn, inprogress_label_var = self.inprogress_var, window=self)
        self.output.insert(ctk.END, ''.join(uploading_output))

        self.upload_button.configure(state="enabled")

    def loading_animetion(self, speed=0.3):
        time_difference = self.loading_animetion_prevtime - datetime.datetime.now()
        if abs(time_difference.total_seconds()) < speed:
            return

        # text = ''
        if self.loading_count == 0:
            text = '⦿'
        elif self.loading_count == 1:
            text = '⦿⦿'
        elif self.loading_count == 2:
            text = '⦿⦿⦿'

        self.loading_count = (self.loading_count + 1) % 3

        self.inprogress_var.set(text)
        self.update()
        
        self.loading_animetion_prevtime = datetime.datetime.now()
