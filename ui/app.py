import json
import customtkinter as ctk
from .zM_input import zM_input

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x500")
        self.title("Configure IBIS controller")

        with open('data.json', 'r',  encoding='utf-8') as file:
            self.data = json.load(file)
            # self.data = json.loads(string)

        self.zM_frame = ctk.CTkScrollableFrame(self)

        for index, item in enumerate(self.data['zM_texts']):
            zM_input_frame = zM_input(self.zM_frame, item, index)
            zM_input_frame.pack(fill='x', padx=10, pady=5)

        self.zM_frame.pack(fill='both', expand=True)
            

