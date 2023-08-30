import customtkinter as ctk
from PIL import Image

class zM_input(ctk.CTkFrame):
    def __init__(self, parent, data, zM_inputs_list, new=False):
        super().__init__(parent, 
                         fg_color='#4d4d4d',
                         corner_radius=15)
        
        self.data = data
        self.zM_inputs_list = zM_inputs_list

        self.index = len(zM_inputs_list)
        if new:
            self.inputs_frame = Inputs(self, {"sign":"","lcd":"","inactive":False})
        else:
            self.inputs_frame = Inputs(self, self.data['zM_texts'][self.index])
        self.order_frame = Order_frame(self, self.index)
        self.hide_remove = Hide_remove(self)

        self.hide_remove.remove_button.bind('<Button-1>', self.remove_self)
        self.order_frame.up_button.bind('<Button-1>', self.move_up)
        self.order_frame.down_button.bind('<Button-1>', self.move_down)

        self.order_frame.pack(side='left', pady=10, padx=10)
        self.inputs_frame.pack(side='left', pady=10, expand=True, fill='both')
        self.hide_remove.pack(side='left', pady=10, padx=10, ipadx=3, ipady=3)

    def remove_self(self, event):
        self.zM_inputs_list.pop(self.index)
        self.data['zM_texts'].pop(self.index)
            
        for i in range(self.index, len(self.zM_inputs_list)):
            self.zM_inputs_list[i].order_frame.number.set(f'{i+1}')
            self.zM_inputs_list[i].index = i

        self.destroy()

    def move_up(self, event):
        if self.index == 0: return

        a = self.index
        b = self.index-1
        
        self.swap_zMs(a, b)

    def move_down(self, event):
        if self.index == len(self.zM_inputs_list)-1: return
        
        a = self.index
        b = self.index+1

        self.swap_zMs(a, b)

    def swap_zMs(self, a, b):
        temp_sign_text = self.zM_inputs_list[a].inputs_frame.sign_input_var.get()
        temp_lcd_text = self.zM_inputs_list[a].inputs_frame.lcd_input_var.get()

        self.zM_inputs_list[a].inputs_frame.sign_input_var.set(self.zM_inputs_list[b].inputs_frame.sign_input_var.get())
        self.zM_inputs_list[a].inputs_frame.lcd_input_var.set(self.zM_inputs_list[b].inputs_frame.lcd_input_var.get())

        self.zM_inputs_list[b].inputs_frame.sign_input_var.set(temp_sign_text)
        self.zM_inputs_list[b].inputs_frame.lcd_input_var.set(temp_lcd_text)

class Order_frame(ctk.CTkFrame):
    def __init__(self, parent, index):
        super().__init__(parent, fg_color='transparent')

        self.number = ctk.StringVar(value=index+1)

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
                                   textvariable=self.number,
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

        # update length
        self.sign_input_var.trace_add('write', lambda *args: self.update_sign_length_label(self, *args))
        self.lcd_input_var.trace_add('write', lambda *args: self.update_lcd_length_label(self, *args))

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

    def update_sign_length_label(self, *args):
        self.sing_input_length_var.set(len(self.sign_input_var.get()))
        
    def update_lcd_length_label(self, *args):
        self.lcd_input_length_var.set(len(self.lcd_input_var.get()))


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