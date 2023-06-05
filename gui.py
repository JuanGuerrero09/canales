from typing import Optional, Tuple, Union
from sympy import Symbol
import customtkinter
import tkinter
from hidraulica_canales import calcular_seccion

class MyEntries(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.values = values 
        definition = {
            'n': 'Rugosidad',
            'Q / yn': 'Caudal o altura',
            'b': 'Ancho de base',
            'So': 'Pendiente',
            'z': 'Talud',
            'D': 'Diametro'
        }
        self.entries = {}

        for i, value in enumerate(self.values):
            entry_frame = customtkinter.CTkFrame(self)
            entry_frame.grid(row=1, column=i, padx=10, pady=(10, 0), sticky="w")
            entry_label = customtkinter.CTkLabel(entry_frame, text=definition[value])
            entry_label.grid(row=0)
            entry = customtkinter.CTkEntry(entry_frame, placeholder_text=value)
            entry.grid(row=1)
            self.entries[value] = entry

    def get(self):
        entry_values = {}
        for key, entry in self.entries.items():
            entry_values[key] = entry.get()
        return entry_values
    
class Selecciones(customtkinter.CTkFrame):
    disable = {
        'Rectangular': ['z', 'D'],
        'Triangular': ['D', 'b'],
        'Trapezoidal': [],
        'Circular': ['z', 'b'],
    }
    def __init__(self, master):
        super().__init__(master)
        selecciones_label = customtkinter.CTkLabel(self, text='Tipo de canal')
        selecciones_label.grid(row=0, column=0)
        self.tipo_de_canal = customtkinter.CTkComboBox(self, values=['Rectangular', 'Trapezoidal', 'Triangular', 'Circular'])
        self.tipo_de_canal.grid(row=0, column=1)

        self.calculo_var = customtkinter.StringVar(value="")

        tipo_de_calculo = customtkinter.CTkRadioButton(self, value='yn', text='Calculo yn', variable=self.calculo_var)
        tipo_de_calculo2 = customtkinter.CTkRadioButton(self, value='Q', text='Calculo caudal', variable=self.calculo_var)
        tipo_de_calculo.grid(row=0, column=2)
        tipo_de_calculo2.grid(row=1, column=2)

    def get(self):
        return self.tipo_de_canal.get(), self.calculo_var.get()

    def set(self, value):
        self.calculo_var.set(value)


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

        self.parameters = customtkinter.CTkFrame(self)
        self.parameters.grid(row=2, columnspan=2)

        self.hydraulic_parameters = MyEntries(self.parameters, values=['n', 'So', 'Q / yn'])
        self.hydraulic_parameters.grid(row=0, column=0)
        self.geometric_parameters = MyEntries(self.parameters, values=['b', 'z', 'D'])
        self.geometric_parameters.grid(row=1, column=0)
        
        self.button = customtkinter.CTkButton(self, text="Calc Value", command=self.button_callback)
        self.button.grid(row=4, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        


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
        seccion_calculada = calcular_seccion(seccion, calculo, n_input, So_input, Q_input, b_input, z_input, D_input)

        
        


app = App()
app.mainloop()