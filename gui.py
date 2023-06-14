import tkinter as tk
from tkinter import ttk
from custom_components import CustomEntry
from gui_open_flow import OpenFlowGui

import sys
sys.path.append('modules')

import utils
from excel_export import generate_report

# Ahora puedes usar las funciones y variables definidas en modulo.py


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hydrosolve")
        self.geometry("680x300")
        self.grid_columnconfigure((0, 1), weight=1)

        self.title_label = tk.Label(self, text='Hydrosolve', justify='center', height=2, font=('Helvetica 16 bold'))
        self.title_label.grid(row=0, columnspan=2)


        self.flow_type_label = tk.Label(self, text='Flow type: ', justify='left')
        self.flow_type_label.grid(row=1)
        self.flow_type = ttk.Combobox(self, values=['Open Channel Flow', 'Pipe Flow'], font="Arial 12")
        self.flow_type.bind("<<ComboboxSelected>>", self.select_flow)
        self.flow_type.current(0)
        self.flow_type.grid(row=1, column=1)

        self.open_flow = OpenFlowGui(self)
        self.pipe_flow = PipeFlow(self)
        
        self.select_flow(event=None)


    def select_flow(self, event):
        selected_flow = self.flow_type.get()
        if selected_flow == 'Open Channel Flow':
            self.open_flow.grid(row=2, columnspan=2)
            self.pipe_flow.grid_forget()
        elif selected_flow == 'Pipe Flow':
            self.pipe_flow.grid(row=2, columnspan=2)
            self.open_flow.grid_forget()


class PipeFlow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.results_title = tk.Label(self, text='PIPE gui', width=25, justify='left', font=("Arial", 16), anchor="w")
        self.results_title.grid(row=0, column=0, sticky='n')







app = App()
app.mainloop()