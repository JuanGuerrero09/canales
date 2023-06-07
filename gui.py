from typing import Optional, Tuple, Union
from sympy import Symbol
import customtkinter
import tkinter as tk
import turtle
from tkinter import ttk
from tkinter import messagebox 
from hidraulica_canales import calcular_seccion
from math import sqrt, atan, degrees, radians
from ilustraciones import draw_trapezoidal_channel, draw_circle, draw_triangle, draw_rectangular

class MyEntries(customtkinter.CTkFrame):
    def __init__(self, master, values, section = None, calculation=None):
        super().__init__(master)
        self.values = values 
        self.section = section
        definition = {
            'n': 'Rugosidad',
            'Q': 'Caudal',
            'yn': 'Altura',
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
            calc = 'Q' if calculation == 'Q' else 'yn'
            if value == calc:
                continue
            entry_frame = customtkinter.CTkFrame(self)
            entry_frame.grid(row=1, column=i, padx=10, pady=(10, 0), sticky="w")
            entry_label = customtkinter.CTkLabel(entry_frame, text=definition[value])
            entry_label.grid(row=0)
            entry = customtkinter.CTkEntry(entry_frame, placeholder_text=value)
            if value in exclude: 
                entry.configure(state='disabled') 
            entry.grid(row=1)
            self.entries[value] = [entry, entry_label]

    def show_entries(self, exclude):
        for value in self.entries:
            entry = self.entries[value][0]
            disabled_values = self.disable[exclude]
            if value not in disabled_values: 
                entry.configure(state='normal') 
            else:
                entry.configure(state='disabled') 

    def change_calculation(self, calc):
        old_calc = 'yn' if calc == 'Q' else 'Q'
        self.entries[old_calc] = self.entries[calc]
        text = 'Altura' if calc == 'Q' else 'Caudal'
        self.entries[old_calc][0].configure(placeholder_text=old_calc)
        self.entries[old_calc][1].configure(text=text)
        del self.entries[calc]



    def get(self):
        entry_values = {}
        entry_labels = {}
        for key, entry in self.entries.items():
            # print(key, entry[0].get(), entry[1].cget('text'))
            entry_values[key] = entry[0].get()
            entry_labels[key] = entry[1].cget('text')
        return entry_values
    
class Selecciones(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        selecciones_label = customtkinter.CTkLabel(self, text='Tipo de canal', anchor='center')
        selecciones_label.grid(row=0, column=0, sticky="ns" )
        self.tipo_de_canal = ttk.Combobox(self, values=['Rectangular', 'Trapezoidal', 'Triangular', 'Circular'])
        self.tipo_de_canal.current(1)
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

class Canvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=300, height=300)
        self.create_turtle()

    def create_turtle(self):
        turtle_screen = self.get_turtle_screen()
        turtle_canvas = turtle_screen.getcanvas()

    def get_turtle_screen(self):
        turtle_screen = turtle.TurtleScreen(self)
        turtle_screen.bgcolor("white")
        turtle_screen.delay(0)
        return turtle_screen

    def draw_channel(self, section):
        canal = section.get('tipo_canal')
        yn = section.get('y')
        b = section.get('b')
        z = section.get('z')
        diameter = section.get('D')
        angle = degrees(section.get('theta')) if section.get('theta') != None else None

        match canal:
            case 'Trapezoidal':
                draw_trapezoidal_channel(yn=yn, z=z, b=b, turtle_screen=self.get_turtle_screen())
            case 'Circular':
                draw_circle(diameter=diameter, angle=angle, turtle_screen=self.get_turtle_screen())
            case 'Rectangular':
                draw_rectangular(yn=yn, b=b, turtle_screen=self.get_turtle_screen())
            case 'Triangular':
                draw_triangle(yn=yn, z=z,turtle_screen=self.get_turtle_screen())
        
        # self.delete(tk.ALL)
        # draw_trapezoidal_channel(yn=0.5, z=0.5, b=2, turtle_screen=self.get_turtle_screen())
        # draw_triangle(yn=1.5, z=0.5, turtle_screen=self.get_turtle_screen())
        # draw_circle(diameter=2, angle=40, turtle_screen=self.get_turtle_screen())
        # draw_rectangular(yn=1.5, b=2, turtle_screen=self.get_turtle_screen())





class Dialogo():
    def __init__(self, text):
        self.text = text

    def show(self):
        # Crear la ventana del diálogo
        # dialog = tk.Toplevel()
        # dialog.title("Canal Trapezoidal")

        # # Crear el widget Canvas dentro del diálogo
        # canvas = Canvas(dialog)

        # # Llamar a la función para dibujar el canal trapezoidal
        # canvas.draw_channel()

        # Mostrar el diálogo
        messagebox.showinfo(title='Resultados', message=self.text)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Canales IDOM")
        self.geometry("500x550")
        self.grid_columnconfigure((0, 1), weight=1)

        self.title = customtkinter.CTkLabel(self, text='Canales IDOM', justify='center', height=35)
        self.title.grid(row=0, columnspan=2)

        self.selecciones = Selecciones(self)
        self.selecciones.grid(row=1, columnspan=2)
        self.selecciones.tipo_de_canal.bind("<<ComboboxSelected>>", self.show_enabled)
        self.selecciones.calculo_var.trace('w', self.select_calc)


        self.parameters = customtkinter.CTkFrame(self)
        self.parameters.grid(row=2, columnspan=2)
        self.section = 'Trapezoidal'
        self.calc = 'yn'

        self.hydraulic_parameters = MyEntries(self.parameters, values=['n', 'So', 'Q', 'yn'])
        self.hydraulic_parameters.grid(row=0, column=0)

        # RENDERIZADO CONDICIONAL
        self.geometric_parameters = MyEntries(self.parameters, values=['b', 'z', 'D'], section=self.section)
        self.geometric_parameters.grid(row=1, column=0)
        #RENDERIZADO CONDICIONAL
        
        self.button = customtkinter.CTkButton(self, text="Calc Value", command=self.button_callback)
        self.button.grid(row=4, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.results_frame = tk.Frame(self)
        self.results_frame.grid(row=5)

        self.canvas = Canvas(self.results_frame)
        self.canvas.grid(row=0, column=0, padx=2)

        self.results = tk.Label(self.results_frame, text='', width=25, justify='left')
        self.results.grid(row=0, column=1, sticky='w', pady=10, padx=10)
    
    def show_enabled(self, event):
        self.section = self.selecciones.get()[0]
        self.geometric_parameters.show_entries(self.section)

    def select_calc(self, *args):
        self.calc = self.selecciones.calculo_var.get()
        self.hydraulic_parameters.change_calculation(self.calc)




    def button_callback(self):
        hydraulic_params = self.hydraulic_parameters.get()
        geometric_params = self.geometric_parameters.get()
        seccion, calculo = self.selecciones.get()
        n_input = float(hydraulic_params['n'])
        So_input = float(hydraulic_params['So'])
        Q_input = float(hydraulic_params['Q']) if calculo != "Q" and 'Q' in  hydraulic_params else None
        y_input = float(hydraulic_params['yn']) if calculo != "yn" else Symbol('y')
        b_input = float(geometric_params['b']) if geometric_params['b'] != "" else None
        z_input = float(geometric_params['z']) if geometric_params['z'] != "" else None
        D_input = float(geometric_params['D']) if geometric_params['D'] != "" else None
        seccion_calculada = calcular_seccion(seccion, calculo, n_input, So_input, Q_input, b_input, z_input, D_input, y_input)
        self.canvas.draw_channel(seccion_calculada.__dict__)
        self.results.config(text = seccion_calculada, font=("Arial", 12), anchor="w")
        print(seccion_calculada.__dict__['n'])
        print(seccion_calculada.__dict__['Q'])
        print(seccion_calculada.__dict__['y'])
        self.dialog = Dialogo(seccion_calculada)
        # self.dialog = Dialogo(seccion_calculada.__dict__)
        self.dialog.show()
        
        


app = App()
app.mainloop()