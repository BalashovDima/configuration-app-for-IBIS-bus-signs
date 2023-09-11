import customtkinter as ctk
from customtkinter import filedialog
import os

class Bottom_bar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, 
                         fg_color='#333232',
                         height=100,
                         corner_radius=0)
    
        self.data_file_frame = Data_file_frame(self)
        self.arduino_file_frame = Arduino_file_frame(self)

        self.data_file_frame.pack(fill='both', pady=(10,0), padx=10)
        self.arduino_file_frame.pack(fill='both', pady=(10,10), padx=10)

class Data_file_frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent,
                         fg_color='transparent',
                         corner_radius=5)
        
        # tk variables
        self.data_file_path_var = ctk.StringVar()

        # frames
        self.labels_frame = ctk.CTkFrame(self,
                                         fg_color='transparent',
                                         corner_radius=5)
        self.buttons_frame = ctk.CTkFrame(self, fg_color='transparent')

        # widgets
        self.label = ctk.CTkLabel(self.labels_frame, 
                                  text='Data file:', 
                                  font=('Regular', 14, 'bold'))
                                  
        self.path_entry = ctk.CTkEntry(self.labels_frame, 
                                       font=('Regular', 14, 'bold'), 
                                       textvariable=self.data_file_path_var)
        
        self.explore_button = ctk.CTkButton(self.buttons_frame, 
                                            text='Browse', 
                                            command=self.browse_files,
                                            width=40)
        
        self.save_button = ctk.CTkButton(self.buttons_frame, text='Save', width=35)

        # layout
        self.columnconfigure(1, weight=1, uniform='a')
        self.columnconfigure(0, weight=5, uniform='a')
        self.labels_frame.grid(row=0, column=0, sticky='nesw')
        self.buttons_frame.grid(row=0, column=1, sticky='e')

        self.label.pack(side='left', padx = 5)
        self.path_entry.pack(side='left', expand=True, fill='both')

        self.save_button.pack(side='right', padx=0)
        self.explore_button.pack(side='right', padx=5)     

    def browse_files(self):
        self.filename = filedialog.askopenfilename(initialdir = os.path.dirname(__file__)+'/../config-data-files/',
                                                   title = "Select a File",
                                                   filetypes = (("json files","*.json*"),("all files", "*.*")))

        self.data_file_path_var.set(self.filename)
        self.path_entry.xview('end')
       

class Arduino_file_frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent,
                         fg_color='transparent',
                         corner_radius=5)
        
        # tk variables
        self.data_file_path_var = ctk.StringVar()

        # frames
        self.labels_frame = ctk.CTkFrame(self,
                                         fg_color='transparent',
                                         corner_radius=5)
        self.buttons_frame = ctk.CTkFrame(self, fg_color='transparent')
        
        # widgets
        self.label = ctk.CTkLabel(self.labels_frame, 
                                  text='Arduino file:', 
                                  font=('Regular', 14, 'bold'))
                                  
        self.path_entry = ctk.CTkEntry(self.labels_frame, 
                                       font=('Regular', 14, 'bold'), 
                                       textvariable=self.data_file_path_var)
        
        self.explore_button = ctk.CTkButton(self.buttons_frame, 
                                            text='Browse', 
                                            command=self.browse_files,
                                            width=40)
        
        self.modify_button = ctk.CTkButton(self.buttons_frame, text='Modify', width=35)
        self.upload_button = ctk.CTkButton(self.buttons_frame, text='Upload', width=35)

        # layout
        self.columnconfigure(1, weight=2, uniform='a')
        self.columnconfigure(0, weight=5, uniform='a')
        self.labels_frame.grid(row=0, column=0, sticky='nesw')
        self.buttons_frame.grid(row=0, column=1, sticky='e')

        self.label.pack(side='left', padx = 5)
        self.path_entry.pack(side='left', expand=True, fill='both')

        self.upload_button.pack(side='right', padx=0)
        self.modify_button.pack(side='right', padx=5)
        self.explore_button.pack(side='right', padx=0)

        self.data_file_path_var.set(os.path.dirname(os.path.dirname(__file__))+'\\arduino-script\\IBIS-bus-signs.ino')     

    def browse_files(self):
        self.filename = filedialog.askopenfilename(initialdir = os.path.dirname(__file__)+'/../arduino-script/',
                                                   title = "Select a File",
                                                   filetypes = (("arduino files","*.ino*"),("all files", "*.*")))

        self.data_file_path_var.set(self.filename)
        self.path_entry.xview('end')