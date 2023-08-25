import customtkinter as ctk
from .zM_input import zM_input

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x500")
        self.title("Configure IBIS controller")

        self.zM_input = zM_input(self)

        self.zM_input.pack(fill='x', padx=10)
