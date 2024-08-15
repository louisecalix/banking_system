import tkinter as tk
from tkinter import ttk

class WidgetsFactory:
    def create_button(self, parent, text, command=None, width=None, height=None, bg='#c7cccc'):
        return tk.Button(parent, text=text, command=command, width=width, height=height, bg=bg)
    
    def create_label(self, parent, text, font=("Courier", 10), bg='#3a4c4d', foreground='white'):
        label = tk.Label(parent, text=text, bg=bg, foreground=foreground)
        label.configure(font=font)
        return label
    
    def create_entry(self, parent, show='', width=40, bg='white'):
        return tk.Entry(parent, show=show, width=width, bg=bg)
    
    def create_text(self, parent):
        return tk.Text(parent)
    
    def create_combobox(self, parent, values=[], state='readonly'):
        return ttk.Combobox(parent, values=values, state=state)
    
    def create_separator(self, parent, orient):
        return ttk.Separator(parent, _orient=orient)

    def create_frame(self, parent, width=None, height=None, bg="lightgray", bd=None, relief=None):
        frame = tk.Frame(parent, width=width, height=height, bg=bg, bd=bd, relief=relief)
        return frame