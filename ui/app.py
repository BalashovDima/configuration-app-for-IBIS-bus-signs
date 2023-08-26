import json
import customtkinter as ctk
from .zM_input import zM_input
from .bottom_bar import Bottom_bar

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x500")
        self.title("Configure IBIS controller")

        self.data_file = ''

        self.zM_frame = ctk.CTkScrollableFrame(self)
        self.bottom_bar = Bottom_bar(self)

        self.bottom_bar.data_file_frame.explore_button.bind('<Button-1>', self.rerender_zM, add='+')
      

        self.zM_frame.pack(fill='both', expand=True)
        self.bottom_bar.pack(fill='both')

    def rerender_zM(self, event):
        self.data_file = self.bottom_bar.data_file_frame.data_file_path_var.get()

        if self.data_file == '': return

        for widgets in self.zM_frame.winfo_children():
            widgets.destroy()

        with open(self.data_file, 'r',  encoding='utf-8') as file:
            self.data = json.load(file)

        for index, item in enumerate(self.data['zM_texts']):
            zM_input_frame = zM_input(self.zM_frame, item, index)
            zM_input_frame.pack(fill='x', padx=10, pady=5)

            

