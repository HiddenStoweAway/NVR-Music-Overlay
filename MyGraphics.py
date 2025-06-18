import tkinter as tk
from typing import Callable

# for keyboard input
from pynput import keyboard

class Attribute:
    def __init__(self, attribute: str, value):
        self.attribute = attribute
        self.value = value

class Window:
    def __init__(
        self, 
        attributes: list[Attribute] = [
            '-topmost',
            '-fullscreen',
            '-toolwindow',
            '-alpha',
            '-disabled',
            '-transparentcolor'
            '-title'
            ], 
        on_key_press: Callable[[], None] = lambda key: {},
        on_key_release: Callable[[], None] = lambda key: {}
        ):
    
        # initialize window
        self.root = tk.Tk()
        
        attributes_list = [
            '-topmost',
            '-fullscreen',
            '-toolwindow',
            '-alpha',
            '-disabled',
            '-transparentcolor',
        ]
        
        for atr in attributes:
            if atr.attribute in attributes_list:
                self.root.attributes(atr.attribute, atr.value)
            elif atr.attribute == '-backgroundcolor':
                self.root.config(background=atr.value)
            elif atr.attribute == '-title':
                self.root.title == atr.value
                print(atr.value)
                
        # Bind key press events to the root window
        listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)
        listener.start()
    
    def attributes(self, index):
        attributes_list = [
            '-topmost',
            '-fullscreen',
            '-toolwindow',
            '-alpha',
            '-disabled',
            '-transparentcolor'
        ]
        
        if index in attributes_list:
            return self.root.attributes(index)
        else:
            return None
        
    def set_attribute(self, attribute, value):
        attributes_list = [
            '-topmost',
            '-fullscreen',
            '-toolwindow',
            '-alpha',
            '-disabled',
            '-transparentcolor'
        ]
        
        if attribute in attributes_list:
            return self.root.attributes(attribute, value)
        else:
            return None
       
    def run(self):
        self.root.mainloop()
     
class Label:
    def __init__(self, window:Window, position_x: int, position_y: int, text = ''):
        self.lbl = tk.Label(window.root, text=text)
        self.lbl.grid(row=position_y, column=position_x)
        
    def pop(self):
        self.lbl.pack()
        
class InputField:
    def __init__(self, window:Window, position_x: int, position_y: int, maxCharacters = None, textvalue = ''):
        self.text_var = tk.StringVar(value=textvalue)
        self.text_var.trace_add("write", self.onChange)
        
        self.maxCharacters = maxCharacters
        
        self.inf = tk.Entry(window.root, textvariable=self.text_var)
        self.inf.grid(row=position_y, column=position_x)

    def onChange(self, *args):
        print(self.getFieldContents())
        contents = list(self.getFieldContents())
        
        if self.maxCharacters:
            if len(contents) > self.maxCharacters:
                self.text_var.set(contents[len(contents) - 1])
                
        self.textvalue = self.getFieldContents()

    def getFieldContents(self):
        return self.text_var.get()
        
def print_value(self):
    print("Value is:", self.text_var.get())
        
def pop(self):
    self.inf.pack()
                    
class Button:
    def __init__(self, window:Window, position_x: int, position_y: int, text = '', command: Callable = ()):
        self.btn = tk.Button(window.root, text=text, command=command)
        self.btn.grid(row=position_y, column=position_x)
        
    def pop(self):
        self.btn.pack()

class Slider:
    def __init__(self, window:Window, position_x: int, position_y: int, orient='horizontal', startVal=0, endVal=100,command: Callable = ()):
        print(orient)
        if(orient != 'horizontal' and orient != 'vertical'):
            print("Bad Slider Orientation")
            return
        
        self.sld = tk.Scale(window.root, orient=orient, from_=endVal, to=startVal, command=command)
        self.sld.grid(row=position_y, column=position_x)

    def set(self, value):
        self.sld.set(value)
        
    def get(self):
        return self.sld.get()
        
    def pop(self):
        self.sld.pack()
