import customtkinter
from modules.generate_zM_sending_code import generate_zM_sending_code
from modules.generate_zM_LCD_text_code import generate_zM_LCD_text_code
from ui.app import App

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

app = App()

app.mainloop()