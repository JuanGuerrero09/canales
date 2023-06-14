import tkinter as tk
from tkinter import ttk
from custom_components import CustomEntry

import sys
sys.path.append('modules')

import utils
from excel_export import generate_report

# Ahora puedes usar las funciones y variables definidas en modulo.py


class Entries(tk.Frame):
    def __init__(self, master, values, section = None, calculation=None):
        super().__init__(master)
        self.values = values 
        self.section = section
        definition = {
            'f': "Darcy Friction Factor",
            'Q': 'Flow Rate [m3/s]',
            'L': 'Length [m]',
            'ID': 'Internal Diameter [m]',
            'C': 'Hazen-Williams Coef.',
            'e': 'Surface Roughness [m]'
        }
        self.entries = {}

        self.disable = {
            'Darcy-Weisbach': ['C'],
            'Hazen-Williams': ['e'],
        }


        for i, value in enumerate(self.values):
            entry_frame = tk.Frame(self)
            entry_frame.grid(row=1, column=i, padx=10, pady=(10, 0), sticky="w")
            entry_label = tk.Label(entry_frame, text=definition[value])
            entry_label.grid(row=0)
            entry = CustomEntry(entry_frame, placeholder=value)
            if value == 'C' and self.section == 'Darcy-Weisbach':
                entry.config(state='disabled')
            if value == 'e' and self.section == 'Hazen-Williams':
                entry.config(state='disabled')
            entry.grid(row=1)
            self.entries[value] = [entry, entry_label]

    def show_entries(self, exclude):
        for value in self.entries:
            entry = self.entries[value][0]
            disabled_values = self.disable[exclude]
            if value not in disabled_values: 
                entry.configure(state='normal') 
            else:
                entry.delete(0, 'end')
                entry.put_placeholder()
                entry.configure(state='disabled') 



    def get(self):
        entry_values = {}
        entry_labels = {}
        for key, entry in self.entries.items():
            entry_values[key] = entry[0].get()
            entry_labels[key] = entry[1].cget('text')
        return entry_values
    

        

class PipeFlowGui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((0, 1), weight=1)


        self.parameters = tk.Frame(self)
        self.parameters.grid(row=2, columnspan=2)


        self.pipe_parameters = Entries(self.parameters, values=['Q', 'ID', 'L'])
        self.pipe_parameters.grid(row=0, column=0)



        self.method_frame = tk.Frame(self)
        self.method_frame.grid(row=3, columnspan=3, pady=10)

        self.method_type_label = tk.Label(self.method_frame, text='Calculation Method: ')
        self.method_type_label.grid(row=0, column=0)
        self.method_type = ttk.Combobox(self.method_frame, values=['Darcy-Weisbach', 'Hazen-Williams'], font="Arial 12")
        self.method_type.current(0)
        self.section = 'Darcy-Weisbach'
        self.method_type.grid(row=0, column=1)
        self.method_parameters = Entries(self.method_frame, values=['C', 'e'],section=self.section)
        self.method_parameters.grid(row=1, columnspan=2)
        self.method_type.bind("<<ComboboxSelected>>", self.show_enabled)



        # self.method_parameters = Entries(self.parameters, values=['b', 'z', 'ID'], section=self.section)
        # self.method_parameters.grid(row=1, column=0)
        
        self.button = ttk.Button(self, text="Calc Value", command=self.pipe_button_callback)
        self.button.grid(row=4, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.results_frame = tk.Frame(self)
        self.results_frame.grid(row=5, columnspan=2)


        self.results_data = tk.Frame(self.results_frame)
        self.results_data.grid(row=0, column=1, padx=20)
        self.results = tk.Label(self.results_data, text='', width=35, justify='left')
        self.results.grid(row=1, column=0, sticky='w')
        self.results2 = tk.Label(self.results_data, text='', width=35, justify='left')
        self.results2.grid(row=1, column=1, sticky='w')

    
    def show_enabled(self, event):
        self.section = self.method_type.get()
        self.method_parameters.show_entries(self.section)

    def select_calc(self, *args):
        self.calc = self.selecciones.calculo_var.get()
        self.pipe_parameters.change_calculation(self.calc)


    def pipe_button_callback(self):
        pipe_params = self.pipe_parameters.get()
        method_params = self.method_parameters.get()
        L_input = float(pipe_params['L'])
        ID_input = float(pipe_params['ID'])
        Q_input = float(pipe_params['Q']) 
        e_input = float(method_params['e']) if self.section != 'Hazen-Williams' and 'e' in  method_params else None
        C_input = float(method_params['C']) if self.section != 'Darcy-Weisbach' and 'C' in  method_params else None
        self.calculated_pipe = utils.calculate_pipe(self.section, L_input,  ID_input, Q_input,  e_input, C_input )
        self.results_title = tk.Label(self.results_data, text='Results: ', width=25, justify='left', font=("Arial", 16))
        self.results_title.grid(row=0, columnspan=2, sticky='n')
        self.results.config(text = utils.formater_str(self.calculated_pipe.__dict__, ['method','Q', 'ID', 'L', 'e', 'C', 'eD']), font=("Arial", 12), anchor="w")
        self.results2.config(text = utils.formater_str(self.calculated_pipe.__dict__, ['Re', 'fr', 'flow_type', 'h', 'hf']), font=("Arial", 12), anchor="w")
        self.more_results_button = tk.Button(self, text="Export to Excel", command=self.export_excel)
        self.more_results_button.grid(row=6, column=0,  padx=20, pady=0, sticky="ew" ,columnspan=2)
        self.master.geometry('680x470')

    def export_excel(self):
        generate_report(self.calculated_pipe.__dict__, 'PipeFlow')

