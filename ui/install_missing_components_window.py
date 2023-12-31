import os
import datetime
import threading
import subprocess
import customtkinter as ctk
from modules.install_arduino_cli import install_arduino_cli

class Install_missing_components_window(ctk.CTkToplevel):
    def __init__(self, parent, missing_components):
        super().__init__(parent)

        self.geometry('670x370')
        self.resizable(False, False)
        self.title('Install missing components')

        self.missing_components = missing_components
        self.missing_components_widgets = []

        # base layout 
        self.installation_settings_frame = ctk.CTkScrollableFrame(self)
        self.output = ctk.CTkTextbox(self)

        self.columnconfigure(0, weight=40, uniform='a')
        self.columnconfigure(1, weight=60, uniform='a')
        self.rowconfigure(0, weight=1)

        self.installation_settings_frame.grid(row=0, column=0, sticky='nsew')
        self.output.grid(row=0, column=1, sticky='nsew')

        # missing components
        if self.missing_components['cli']:
            self.missing_components_widgets.append(Component(self.installation_settings_frame, 'Arduino command line tool:', ['arduino-cli']))
        if self.missing_components['avr-core']:
            self.missing_components_widgets.append(Component(self.installation_settings_frame, 'Arduino AVR core:', ['avr-core']))
        if len(self.missing_components['libs']):
            libraries = []
            for lib in self.missing_components['libs']:
                libraries.append(f'{lib["name"]}@{lib["version"]}')
            self.missing_components_widgets.append(Component(self.installation_settings_frame, 'Missing libraries:', libraries))
        if len(self.missing_components['wrong-version-libs']):
            libraries = []
            for lib in self.missing_components['wrong-version-libs']:
                libraries.append(f'{lib["name"]}@{lib["version"]}')
            self.missing_components_widgets.append(Component(self.installation_settings_frame, 'Wrong version libraries:', libraries))

        for component in self.missing_components_widgets:
            component.pack(expand=True, fill='x')

        # install button (end)
        self.install_button = ctk.CTkButton(self.installation_settings_frame, text='Install', width=40, command=self.install)
        self.install_button.pack(anchor='e', pady=(10,0))

        # inprogress indication
        self.loading_animetion_prevtime = datetime.datetime.now()
        self.loading_count = 1
        self.inprogress_var = ctk.StringVar(value='')
        self.inprogress = ctk.CTkFrame(self)
        self.inprogress_label = ctk.CTkLabel(self.inprogress, textvariable = self.inprogress_var, font=('Calibri', 20))
        self.inprogress_label.pack(padx=15, pady=7)

        # done button
        self.done_button = ctk.CTkButton(self, text='Done', width=45)
        x_coordinate = self.winfo_width() - 10 - self.done_button.winfo_reqwidth()
        y_coordinate = self.winfo_height() - 10 - self.done_button.winfo_reqheight()
        self.done_button.place(x=x_coordinate, y=y_coordinate)

    def install(self):
        def function_to_run_in_background():
            self.install_button.configure(state="disabled")

            remove_from_components = []
            # for each section (cli, core, libs, wrong libs)
            for i, component in enumerate(self.missing_components_widgets):
                # CLI
                if component.component_type == 'arduino-cli':
                    if component.checkbox_vars[0].get():
                        self.output.insert('end', 'Installing arduino-cli...\n')
                        installation_result, output_text = install_arduino_cli(os.getcwd())
                        self.output.insert('end', output_text+'\n')

                        if installation_result:
                            try:
                                process = subprocess.Popen("arduino-cli config init", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                stdout, stderr = process.communicate()

                                if process.returncode == 0:
                                    self.output.insert('end', stdout + '\n')
                                    print(stdout)
                                else:
                                    self.output.insert('end', stderr)
                                    self.output.insert('end', str(process.returncode) + '\n')
                                    print(stderr)
                                    print(process.returncode)

                            except subprocess.CalledProcessError as e:
                                self.output.insert('end', e.stderr + '')
                                self.output.insert('end', str(e) + '\n')
                                print(e.stderr)
                                print(e)

                            component.destroy()
                            remove_from_components.append(i)
                # CORE
                if component.component_type == 'avr-core':
                    if component.checkbox_vars[0].get():
                        self.output.insert('end', 'Installing arduino AVR core...\n Confirm installation of drivers when you are prompted to.\n')
                        try:
                            process = subprocess.Popen("arduino-cli core install arduino:avr", shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                            stdout, stderr = process.communicate()

                            if process.returncode == 0:
                                self.output.insert('end', stdout + '\n')
                                print(stdout)
                                component.destroy()
                                remove_from_components.append(i)
                            else:
                                self.output.insert('end', stderr)
                                self.output.insert('end', str(process.returncode) + '\n')
                                print(stderr)
                                print(process.returncode)

                        except subprocess.CalledProcessError as e:
                            self.output.insert('end', e.stderr + '')
                            self.output.insert('end', str(e) + '\n')
                            print(e.stderr)
                            print(e)

                # LIBS and WRONG LIBS
                if component.component_type == 'libs' or component.component_type == 'wrong-version-libs':
                    successfully_installed = []
                    # for each checkbox (each library)
                    for lib_i, checkbox_var in enumerate(component.checkbox_vars):
                        # if library checked, then install it
                        if checkbox_var.get(): 
                            try:
                                process = subprocess.Popen(f'arduino-cli lib install "{component.checkbox_texts[lib_i]}"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                stdout, stderr = process.communicate()

                                if process.returncode == 0:
                                    self.output.insert('end', stdout + '\n')
                                    print(stdout)
                                    # mark this library as successfully installed (to then remove it from the list of the ones that need to be installed)
                                    successfully_installed.append(lib_i)
                                else:
                                    self.output.insert('end', stderr)
                                    self.output.insert('end', str(process.returncode) + '\n')
                                    print(stderr)
                                    print(process.returncode)

                            except subprocess.CalledProcessError as e:
                                self.output.insert('end', e.stderr + '')
                                self.output.insert('end', str(e) + '\n')
                                print(e.stderr)
                                print(e)


                    # remove successfully installed libraries from the list of options
                    successfully_installed.reverse()
                    for lib in successfully_installed:
                        component.checkbox_list[lib].destroy()
                        component.checkbox_list.pop(lib)
                        component.checkbox_texts.pop(lib)
                        component.checkbox_vars.pop(lib)
                    
                    # if all libraries were installed then remove (and add to remove list) the sections with libraries
                    if not len(component.checkbox_list):
                        component.destroy()
                        remove_from_components.append(i)
            

            # remove from the list of sections the ones that were installed
            for i in remove_from_components:
                self.missing_components_widgets.pop(i)
                
            self.install_button.configure(state="normal")

        self.inprogress.place(x=0, y=0)
        thread = threading.Thread(target=function_to_run_in_background)
        thread.start()
        while thread.is_alive(): # display animetion while prerequisites are being checked
            self.loading_animetion()
        self.inprogress.place_forget()
        thread.join()

    def loading_animetion(self, speed=0.3):
        time_difference = self.loading_animetion_prevtime - datetime.datetime.now()
        if abs(time_difference.total_seconds()) < speed:
            return

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

class Component(ctk.CTkFrame):
    def __init__(self, parent, label_text, checkbox_items):
        super().__init__(parent)

        if label_text == 'Arduino command line tool:': self.component_type = 'arduino-cli'
        elif label_text == 'Arduino AVR core:': self.component_type = 'avr-core'
        elif label_text == 'Missing libraries:': self.component_type = 'libs'
        elif label_text == 'Wrong version libraries:': self.component_type = 'wrong-version-libs'

        self.checkbox_texts = checkbox_items
        self.checkbox_vars = []
        self.checkbox_list = []

        self.label = ctk.CTkLabel(self, text=label_text, font=('Calibri', 18))
        self.label.pack(anchor='w')

        self.checkbox_frame = ctk.CTkFrame(self)
        self.checkbox_frame.pack(expand=True, padx=(20,0), fill='x')
        for i, checkbox_item in enumerate(self.checkbox_texts):
            state_var = ctk.BooleanVar(value=True)
            if self.component_type == 'wrong-version-libs': state_var.set(False)
            checkbox = ctk.CTkCheckBox(self.checkbox_frame, text=checkbox_item, variable=state_var)
            # add padding on top for each checkbox starting from second (index 1+)
            if i: checkbox.pack(anchor='w', pady=(5,0))
            else: checkbox.pack(anchor='w')

            self.checkbox_vars.append(state_var)
            self.checkbox_list.append(checkbox)
