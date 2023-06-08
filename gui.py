from sympy import Symbol
import tkinter as tk
import turtle
from tkinter import ttk
from hidraulica_canales import calcular_seccion
from math import sqrt, atan, degrees, radians
from ilustraciones import draw_trapezoidal_channel, draw_circle, draw_triangle, draw_rectangular
from custom_components import CustomEntry

class MyEntries(tk.Frame):
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
            entry_frame = tk.Frame(self)
            entry_frame.grid(row=1, column=i, padx=10, pady=(10, 0), sticky="w")
            entry_label = tk.Label(entry_frame, text=definition[value])
            entry_label.grid(row=0)
            entry = CustomEntry(entry_frame, placeholder=value)
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
                entry.delete(0, 'end')
                entry.put_placeholder()
                entry.configure(state='disabled') 

    def change_calculation(self, calc):
        old_calc = 'yn' if calc == 'Q' else 'Q'
        self.entries[old_calc] = self.entries[calc]
        text = 'Altura' if calc == 'Q' else 'Caudal'
        self.entries[old_calc][0].placeholder=old_calc
        self.entries[old_calc][0].set_placeholder()
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
    
class Selecciones(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        selecciones_label = tk.Label(self, text='Tipo de canal', anchor='center')
        selecciones_label.grid(row=0, column=0, sticky="ns" )
        self.tipo_de_canal = ttk.Combobox(self, values=['Rectangular', 'Trapezoidal', 'Triangular', 'Circular'], font="Arial 12")
        self.tipo_de_canal.current(1)
        self.tipo_de_canal.grid(row=0, column=1, padx= 30)

        self.calculo_var = tk.StringVar(value="yn")

        self.tipo_de_calculo_frame = tk.Frame(self)
        self.tipo_de_calculo_frame.grid(row=0, column=2)
        tipo_de_calculo = tk.Radiobutton(self.tipo_de_calculo_frame, value='yn', text='Calculo yn', variable=self.calculo_var)
        tipo_de_calculo2 = tk.Radiobutton(self.tipo_de_calculo_frame, value='Q', text='Calculo caudal', variable=self.calculo_var)
        tipo_de_calculo.grid(row=0, column=2, sticky="w")
        tipo_de_calculo2.grid(row=1, column=2, sticky="w")

    def get(self):
        return self.tipo_de_canal.get(), self.calculo_var.get()

    def set(self, value):
        self.calculo_var.set(value)

class Canvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=250, height=250)
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
        



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Canales IDOM")
        self.geometry("550x550")
        self.grid_columnconfigure((0, 1), weight=1)

        self.title = tk.Label(self, text='Canales IDOM', justify='center', height=2)
        self.title.grid(row=0, columnspan=2)

        self.selecciones = Selecciones(self)
        self.selecciones.grid(row=1, columnspan=2)
        self.selecciones.tipo_de_canal.bind("<<ComboboxSelected>>", self.show_enabled)
        self.selecciones.calculo_var.trace('w', self.select_calc)


        self.parameters = tk.Frame(self)
        self.parameters.grid(row=2, columnspan=2)
        self.section = 'Trapezoidal'
        self.calc = 'yn'

        self.hydraulic_parameters = MyEntries(self.parameters, values=['n', 'So', 'Q', 'yn'])
        self.hydraulic_parameters.grid(row=0, column=0)

        # RENDERIZADO CONDICIONAL
        self.geometric_parameters = MyEntries(self.parameters, values=['b', 'z', 'D'], section=self.section)
        self.geometric_parameters.grid(row=1, column=0)
        #RENDERIZADO CONDICIONAL
        
        self.button = ttk.Button(self, text="Calc Value", command=self.button_callback)
        self.button.grid(row=4, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.results_frame = tk.Frame(self)
        self.results_frame.grid(row=5, columnspan=2)

        self.canvas = Canvas(self.results_frame)
        self.canvas.grid(row=0, column=0, padx=2)
        self.canvas.create_text(101, -93, text="z", fill="black", font=('Helvetica 14 bold'))
        self.canvas.create_text(116, -110, text="1", fill="black", font=('Helvetica 14 bold'))
        self.canvas.create_polygon(110, -100, 110, -120, 90, -100)

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
        b_input = float(geometric_params['b']) if not geometric_params['b'].isalpha()  else None
        z_input = float(geometric_params['z']) if not geometric_params['z'].isalpha()  else None
        D_input = float(geometric_params['D']) if not geometric_params['D'].isalpha()  else None
        seccion_calculada = calcular_seccion(seccion, calculo, n_input, So_input, Q_input, b_input, z_input, D_input, y_input)
        self.canvas.draw_channel(seccion_calculada.__dict__)
        self.results.config(text = seccion_calculada, font=("Arial", 12), anchor="w")
        
        


app = App()
app.mainloop()