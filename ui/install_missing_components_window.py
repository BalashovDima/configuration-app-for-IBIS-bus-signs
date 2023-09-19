import customtkinter as ctk

class Install_missing_components_window(ctk.CTkToplevel):
    def __init__(self, parent, missing_components):
        super().__init__(parent)

        self.geometry('520x370')
        self.resizable(False, False)
        self.title('Install missing components')

        self.missing_components = missing_components

        self.done_button = ctk.CTkButton(self, text='Done')
        x_coordinate = 520 - 10 - self.done_button.winfo_reqwidth()
        y_coordinate = 370 - 10 - self.done_button.winfo_reqheight()
        self.done_button.place(x=x_coordinate, y=y_coordinate)