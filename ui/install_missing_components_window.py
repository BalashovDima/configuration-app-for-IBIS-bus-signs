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

        # done button
        self.done_button = ctk.CTkButton(self, text='Done', width=45)
        x_coordinate = self.winfo_width() - 10 - self.done_button.winfo_reqwidth()
        y_coordinate = self.winfo_height() - 10 - self.done_button.winfo_reqheight()
        self.done_button.place(x=x_coordinate, y=y_coordinate)

    def install(self):
        self.output.insert('end', 'Installing...')

class Component(ctk.CTkFrame):
    def __init__(self, parent, label_text, checkbox_items):
        super().__init__(parent)

        self.checkbox_list = []

        self.label = ctk.CTkLabel(self, text=label_text, font=('Calibri', 18))
        self.label.pack(anchor='w')

        self.checkbox_frame = ctk.CTkFrame(self)
        self.checkbox_frame.pack(expand=True, padx=(20,0), fill='x')
        for i, checkbox_item in enumerate(checkbox_items):
            checkbox = ctk.CTkCheckBox(self.checkbox_frame, text=checkbox_item)
            checkbox.select()
            # add padding on top for each checkbox starting from second (index 1+)
            if i: checkbox.pack(anchor='w', pady=(5,0))
            else: checkbox.pack(anchor='w')

            self.checkbox_list.append(checkbox)
