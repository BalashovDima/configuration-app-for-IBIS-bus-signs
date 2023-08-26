import customtkinter as ctk
from PIL import Image

class zM_input(ctk.CTkFrame):
    def __init__(self, parent, data, index):
        super().__init__(parent, 
                         fg_color='#4d4d4d',
                         corner_radius=15)
        
        self.data = data
        self.index = index

        self.order_frame = Order_frame(self, self.index)
        self.inputs_frame = Inputs(self, self.data)
        self.hide_remove = Hide_remove(self)

        self.order_frame.pack(side='left', pady=10, padx=10)
        self.inputs_frame.pack(side='left', pady=10, expand=True, fill='both')
        self.hide_remove.pack(side='left', pady=10, padx=10, ipadx=3, ipady=3)


class Order_frame(ctk.CTkFrame):
    def __init__(self, parent, number):
        super().__init__(parent, fg_color='transparent')

        self.number = number

        up_icon_light = Image.open('icons/up-light.png')
        down_icon_light = Image.open('icons/down-light.png')
        ctk_up_icon_light = ctk.CTkImage(up_icon_light, size=(24,24))
        ctk_down_icon_light = ctk.CTkImage(down_icon_light, size=(24,24))

        self.up_button = ctk.CTkButton(self, 
                                       image=ctk_up_icon_light, 
                                       text=None, 
                                       width=20, 
                                       height=30, 
                                       fg_color='transparent', 
                                       corner_radius=5)
        self.down_button = ctk.CTkButton(self, 
                                         image=ctk_down_icon_light, 
                                         text=None, 
                                         width=20, 
                                         height=30, 
                                         fg_color='transparent', 
                                         corner_radius=5)
        self.number_widget = ctk.CTkLabel(self,
                                   text=self.number+1,
                                   width=30,
                                   height=30,
                                   font=('Calibri', 24),
                                   text_color='#FFFFFF')

        self.up_button.pack()
        self.number_widget.pack()
        self.down_button.pack()

class Inputs(ctk.CTkFrame):
    def __init__(self, parent, data):
        super().__init__(parent, fg_color='transparent')

        self.data = data

        # tk variables
        self.sign_input_var = ctk.StringVar(value=data['sign'])
        self.lcd_input_var = ctk.StringVar(value=data['lcd'])
        self.sing_input_length_var = ctk.IntVar(value=len(self.sign_input_var.get()))
        self.lcd_input_length_var = ctk.IntVar(value=len(self.lcd_input_var.get()))

        # grid configuration
        self.rowconfigure((0,2), weight=7, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=17)

        # labels 
        sign_label = ctk.CTkLabel(self, text='SIGN')
        lcd_label = ctk.CTkLabel(self, text='LCD')

        sign_label.grid(row=0, column=0, sticky='w')
        lcd_label.grid(row=2, column=0, sticky='w')
        
        # inputs
        self.sign_inputs_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.lcd_inputs_frame = ctk.CTkFrame(self, fg_color='transparent')
        
        self.sign_input = ctk.CTkEntry(self.sign_inputs_frame, font=('Regular', 14), textvariable=self.sign_input_var)
        self.lcd_input = ctk.CTkEntry(self.lcd_inputs_frame, font=('Regular', 14), textvariable=self.lcd_input_var)

        self.sign_input.pack(side='left', expand=True, fill='both')
        self.lcd_input.pack(side='left',fill='both')
        
        self.sign_input_length = ctk.CTkLabel(self.sign_inputs_frame, textvariable = self.sing_input_length_var)
        self.lcd_input_length = ctk.CTkLabel(self.lcd_inputs_frame, textvariable = self.lcd_input_length_var)

        self.sign_input_length.pack(side='left')
        self.lcd_input_length.pack(side='left')
        self.sign_inputs_frame.grid(row=0, column=1, sticky='nesw')
        self.lcd_inputs_frame.grid(row=2, column=1, sticky='nesw')


class Hide_remove(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color='#666666', corner_radius=5)

        disable_icon_light = Image.open('icons/disable-light.png')
        trash_icon_light = Image.open('icons/trash-light.png')
        ctk_disable_icon_light = ctk.CTkImage(disable_icon_light, size=(24,24))
        ctk_trash_icon_light = ctk.CTkImage(trash_icon_light, size=(24,24))

        self.disable_button = ctk.CTkButton(self, 
                                       image=ctk_disable_icon_light, 
                                       text=None, 
                                       width=20, 
                                       height=30, 
                                       fg_color='transparent', 
                                       corner_radius=5)
        self.remove_button = ctk.CTkButton(self, 
                                         image=ctk_trash_icon_light, 
                                         text=None, 
                                         width=20, 
                                         height=30, 
                                         fg_color='transparent', 
                                         corner_radius=5)

        self.disable_button.pack(pady=5)
        self.remove_button.pack()