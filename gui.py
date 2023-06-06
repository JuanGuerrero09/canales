from typing import Optional, Tuple, Union
from sympy import Symbol
import customtkinter
from tkinter import ttk
from tkinter import messagebox 
from hidraulica_canales import calcular_seccion

class MyEntries(customtkinter.CTkFrame):
    def __init__(self, master, values, section = None):
        super().__init__(master)
        self.values = values 
        self.section = section
        definition = {
            'n': 'Rugosidad',
            'Q / yn': 'Caudal o altura',
            'b': 'Ancho de base',
            'So': 'Pendiente',
            'z': 'Talud',
            'D': 'Diametro'
        }
        self.entries = {}

        self.disable = {
            'Rectangular': ['z', 'D'],
            'Triangular': ['D', 'b'],
            'Trapezoidal': ['D'],
            'Circular': ['z', 'b'],
        }
        for i, value in enumerate(self.values):
            exclude = self.disable[section] if section != None else ['z', 'D', 'b']
            entry_frame = customtkinter.CTkFrame(self)
            entry_frame.grid(row=1, column=i, padx=10, pady=(10, 0), sticky="w")
            entry_label = customtkinter.CTkLabel(entry_frame, text=definition[value])
            entry_label.grid(row=0)
            print(value in exclude)
            entry = customtkinter.CTkEntry(entry_frame, placeholder_text=value)
            if value in exclude: 
                entry.configure(state='disabled') 
            entry.grid(row=1)
            self.entries[value] = entry

    def show_entries(self, exclude):
        print(self.entries)
        for value in self.entries:
            entry = self.entries[value]
            disabled_values = self.disable[exclude]
            print(entry, self.disable[exclude])
            print(value, value in disabled_values)
            if value not in disabled_values: 
                entry.configure(state='normal') 
            else:
                entry.configure(state='disabled') 


    def get(self):
        entry_values = {}
        for key, entry in self.entries.items():
            entry_values[key] = entry.get()
        return entry_values
    
class Selecciones(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        selecciones_label = customtkinter.CTkLabel(self, text='Tipo de canal', anchor='center')
        selecciones_label.grid(row=0, column=0, sticky="ns" )
        self.tipo_de_canal = ttk.Combobox(self, values=['Rectangular', 'Trapezoidal', 'Triangular', 'Circular'])
        self.tipo_de_canal.grid(row=0, column=1, padx= 30)

        self.calculo_var = customtkinter.StringVar(value="yn")

        self.tipo_de_calculo_frame = customtkinter.CTkFrame(self)
        self.tipo_de_calculo_frame.grid(row=0, column=2)
        tipo_de_calculo = customtkinter.CTkRadioButton(self.tipo_de_calculo_frame, value='yn', text='Calculo yn', variable=self.calculo_var)
        tipo_de_calculo2 = customtkinter.CTkRadioButton(self.tipo_de_calculo_frame, value='Q', text='Calculo caudal', variable=self.calculo_var)
        tipo_de_calculo.grid(row=0, column=2, sticky="w")
        tipo_de_calculo2.grid(row=1, column=2, sticky="w")

    def get(self):
        return self.tipo_de_canal.get(), self.calculo_var.get()

    def set(self, value):
        self.calculo_var.set(value)

class Dialogo():
    def __init__(self, text):
        super().__init__()
        self.text = text
    def show(self):
        messagebox.showinfo(title='Resultados', message=self.text)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Canales IDOM")
        self.geometry("500x350")
        self.grid_columnconfigure((0, 1), weight=1)

        self.title = customtkinter.CTkLabel(self, text='Canales IDOM', justify='center', height=35)
        self.title.grid(row=0, columnspan=2)

        self.selecciones = Selecciones(self)
        self.selecciones.grid(row=1, columnspan=2)
        self.selecciones.tipo_de_canal.bind("<<ComboboxSelected>>", self.show_enabled)


        self.parameters = customtkinter.CTkFrame(self)
        self.parameters.grid(row=2, columnspan=2)
        self.section = 'Trapezoidal'

        self.hydraulic_parameters = MyEntries(self.parameters, values=['n', 'So', 'Q / yn'])
        self.hydraulic_parameters.grid(row=0, column=0)

        # RENDERIZADO CONDICIONAL
        self.geometric_parameters = MyEntries(self.parameters, values=['b', 'z', 'D'], section=self.section)
        self.geometric_parameters.grid(row=1, column=0)
        #RENDERIZADO CONDICIONAL
        
        self.button = customtkinter.CTkButton(self, text="Calc Value", command=self.button_callback)
        self.button.grid(row=4, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

    
    def show_enabled(self, event):
        self.section = self.selecciones.get()[0]
        self.geometric_parameters.show_entries(self.section)
        print(self.section)


    def button_callback(self):
        hydraulic_params = self.hydraulic_parameters.get()
        geometric_params = self.geometric_parameters.get()
        seccion, calculo = self.selecciones.get()
        n_input = float(hydraulic_params['n'])
        So_input = float(hydraulic_params['So'])
        Q_input = float(hydraulic_params['Q / yn']) if calculo != "Q" else None
        y_input = float(hydraulic_params['Q / yn']) if calculo != "yn" else Symbol('y')
        b_input = float(geometric_params['b']) if geometric_params['b'] != "" else None
        z_input = float(geometric_params['z']) if geometric_params['z'] != "" else None
        D_input = float(geometric_params['D']) if geometric_params['D'] != "" else None
        print("button pressed", self.hydraulic_parameters.get(), self.geometric_parameters.get(), seccion)
        print(type(b_input))
        print('mi seccion es: ', seccion, calculo, n_input, So_input, Q_input, b_input, z_input, D_input, y_input)
        seccion_calculada = calcular_seccion(seccion, calculo, n_input, So_input, Q_input, b_input, z_input, D_input, y_input)

        self.dialog = Dialogo(seccion_calculada)
        self.dialog.show()
        
        


app = App()
app.mainloop()