import json
from threading import Timer
import customtkinter as ctk
from .zM_input import zM_input
from .bottom_bar import Bottom_bar
from modules.modify_arduino_file import modify_arduino_file
from .upload_window import Upload_window

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x500")
        self.title("Configure IBIS controller")

        self.data_file = ''
        self.zM_inputs_list = []

        self.zM_frame = ctk.CTkScrollableFrame(self)
        self.bottom_bar = Bottom_bar(self)
        self.upload_window = None

        self.bottom_bar.data_file_frame.explore_button.bind('<Button-1>', self.rerender_zM, add='+')
        self.bottom_bar.data_file_frame.save_button.bind('<Button-1>', self.save_data_file, add='+')
        self.bottom_bar.arduino_file_frame.modify_button.bind('<Button-1>', self.modify_arduino_file, add='+')
        self.bottom_bar.arduino_file_frame.upload_button.bind('<Button-1>', self.upload_to_arduino, add='+')
      

        self.zM_frame.pack(fill='both', expand=True)
        self.bottom_bar.pack(fill='both')

    def rerender_zM(self, event):
        self.data_file = self.bottom_bar.data_file_frame.data_file_path_var.get()

        if self.data_file == '': return

        for widgets in self.zM_frame.winfo_children():
            widgets.destroy()

        self.zM_inputs_list.clear()

        with open(self.data_file, 'r',  encoding='utf-8') as file:
            self.data = json.load(file)

        for i in self.data['zM_texts']:
            zM_input_frame = zM_input(self.zM_frame, self.data, self.zM_inputs_list)
            zM_input_frame.pack(fill='x', padx=10, pady=5)

            self.zM_inputs_list.append(zM_input_frame)

        self.render_new_zM_button()
        

    def render_new_zM_button(self):
        self.new_zM_button = ctk.CTkButton(self.zM_frame, 
                                           text='+', 
                                           font=('Regular', 25, 'bold'),
                                           width=50,
                                           height=50,
                                           command=self.add_zM_input)
        self.new_zM_button.pack(side='right', padx=20, pady=20)

    def add_zM_input(self):
        self.new_zM_button.destroy()

        zM_input_frame = zM_input(self.zM_frame, self.data, self.zM_inputs_list, new=True)
        zM_input_frame.pack(fill='x', padx=10, pady=5)

        self.zM_inputs_list.append(zM_input_frame)
        self.data['zM_texts'].append({"sign":"","lcd":"","inactive":False})

        self.render_new_zM_button()

    def save_data_file(self, event):
        self.data_file = self.bottom_bar.data_file_frame.data_file_path_var.get()

        if self.data_file == '': return

        for index, zM_frame in enumerate(self.zM_inputs_list):
            self.data['zM_texts'][index]['sign'] = zM_frame.inputs_frame.sign_input_var.get()
            self.data['zM_texts'][index]['lcd'] = zM_frame.inputs_frame.lcd_input_var.get()

        with open(self.data_file, 'w',  encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

        self.notification('Saved')

    def modify_arduino_file(self, event):
        self.arduino_file = self.bottom_bar.arduino_file_frame.data_file_path_var.get()

        if modify_arduino_file(self.arduino_file, self.data) == 'success':
            self.notification("Successfully modified")
        else:
            self.notification("Couldn't modify")

    def upload_to_arduino(self, event):
        self.data_file = self.bottom_bar.data_file_frame.data_file_path_var.get()
        self.arduino_file = self.bottom_bar.arduino_file_frame.data_file_path_var.get()
        if self.arduino_file == '' or self.data_file == '': 
            self.notification('Choose files')
            return
        
        if self.upload_window is None or not self.upload_window.winfo_exists():
            self.upload_window = Upload_window(self, self.data, self.arduino_file)  # create window if its None or destroyed
            Timer(0.1, lambda:self.upload_window.focus()).start()
        else:
            self.upload_window.focus()  # if window exists focus it

    def notification(self, message):
        def remove_notification(notification):
            notification.destroy()

        notification = ctk.CTkFrame(self)
        notification_text = ctk.CTkLabel(notification, 
                                         text=message, 
                                         font=('Regular', 18),
                                         padx=20,
                                         pady=5)
        notification_text.pack()
        notification.place(relx=0.5, y=30, anchor='center')
        Timer(2.0, remove_notification, args=(notification,)).start()