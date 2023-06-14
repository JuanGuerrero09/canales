from sympy import Symbol
import tkinter as tk
import turtle
from tkinter import ttk
from math import sqrt, atan, degrees, radians
from draws import draw_Trapezoid_channel, draw_circle, draw_triangle, draw_Rectangle, get_img_from_draw
from custom_components import CustomEntry
from PIL import Image, ImageTk

# arreglar flow (Altura)
#triangullo

import sys
sys.path.append('modules')

import utils
from excel_export import generate_report

# Ahora puedes usar las funciones y variables definidas en modulo.py


class MyEntries(tk.Frame):
    def __init__(self, master, values, section = None, calculation=None):
        super().__init__(master)
        self.values = values 
        self.section = section
        definition = {
            'n': "Manning's Coef.",
            'Q': 'Flow Rate [m3/s]',
            'y': 'Depth [m]',
            'b': 'Bottom Width [m]',
            'So': 'Channel Slope [m/m]',
            'z': 'Side Slope 1V:ZH',
            'D': 'Diameter [m]'
        }
        self.entries = {}

        self.disable = {
            'Rectangle': ['z', 'D'],
            'Triangle': ['D', 'b'],
            'Trapezoid': ['D'],
            'Circle': ['z', 'b'],
        }
        for i, value in enumerate(self.values):
            exclude = self.disable[section] if section != None else ['z', 'D', 'b']
            calc = 'Q' if calculation == 'Q' else 'y'
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
        old_calc = 'y' if calc == 'Q' else 'Q'
        self.entries[old_calc] = self.entries[calc]
        text = 'Depth [m]' if calc == 'Q' else 'Flow Rate [m3/s]'
        self.entries[old_calc][0].placeholder=old_calc
        self.entries[old_calc][0].set_placeholder()
        self.entries[old_calc][1].configure(text=text)
        del self.entries[calc]



    def get(self):
        entry_values = {}
        entry_labels = {}
        for key, entry in self.entries.items():
            entry_values[key] = entry[0].get()
            entry_labels[key] = entry[1].cget('text')
        return entry_values
    
class Selecciones(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        selecciones_label = tk.Label(self, text='Select Channel Type:', anchor='center')
        selecciones_label.grid(row=0, column=0, sticky="ns" )
        self.tipo_de_canal = ttk.Combobox(self, values=['Rectangle', 'Trapezoid', 'Triangle', 'Circle'], font="Arial 12")
        self.tipo_de_canal.current(1)
        self.tipo_de_canal.grid(row=0, column=1, padx= 30)

        self.calculo_var = tk.StringVar(value="y")

        self.tipo_de_calculo_frame = tk.Frame(self)
        self.tipo_de_calculo_frame.grid(row=0, column=2)
        tipo_de_calculo = tk.Radiobutton(self.tipo_de_calculo_frame, value='y', text='Calculate Depth', variable=self.calculo_var)
        tipo_de_calculo2 = tk.Radiobutton(self.tipo_de_calculo_frame, value='Q', text='Calculate Flow', variable=self.calculo_var)
        tipo_de_calculo.grid(row=0, column=2, sticky="w")
        tipo_de_calculo2.grid(row=1, column=2, sticky="w")

    def get(self):
        return self.tipo_de_canal.get(), self.calculo_var.get()

    def set(self, value):
        self.calculo_var.set(value)

class Canvas(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=300, height=300)

    def show_image(self):
        img = Image.open('channel.png')
        img = img.resize((215, 215))
        self.pimg = ImageTk.PhotoImage(img)
        self.create_image(0, 0, anchor='nw', image=self.pimg)



    def draw_channel(self, section):
        channel = section.get('channel_type')
        yn = float(section.get('y'))
        b = section.get('b')
        z = section.get('z')
        diameter = section.get('D')
        angle = degrees(section.get('theta')) if section.get('theta') != None else None
        match channel:
            case 'Trapezoidal':
                channel = draw_Trapezoid_channel(yn=yn, z=z, b=b)
            case 'Circular':
                channel = draw_circle(diameter=diameter, angle=angle)
            case 'Rectangular':
                channel = draw_Rectangle(yn=yn, b=b)
            case 'Triangular':
                channel = draw_triangle(yn=yn, z=z)
        channel.save_as('channel.svg')
        #converts svg to png
        get_img_from_draw(channel)
        # #a file called channel.png is created
        self.show_image()

        

class OpenFlowGui(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.selecciones = Selecciones(self)
        self.selecciones.grid(row=1, columnspan=2)
        self.selecciones.tipo_de_canal.bind("<<ComboboxSelected>>", self.show_enabled)
        self.selecciones.calculo_var.trace('w', self.select_calc)


        self.parameters = tk.Frame(self)
        self.parameters.grid(row=2, columnspan=2)
        self.section = 'Trapezoid'
        self.calc = 'y'

        self.hydraulic_parameters = MyEntries(self.parameters, values=['n', 'So', 'Q', 'y'])
        self.hydraulic_parameters.grid(row=0, column=0)

        self.geometric_parameters = MyEntries(self.parameters, values=['b', 'z', 'D'], section=self.section)
        self.geometric_parameters.grid(row=1, column=0)
        
        self.button = ttk.Button(self, text="Calc Value", command=self.button_callback)
        self.button.grid(row=4, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.results_frame = tk.Frame(self)
        self.results_frame.grid(row=5, columnspan=2)

        self.canvas = Canvas(self.results_frame)
        self.canvas.grid(row=0, column=0, padx=(80, 0))
        self.canvas.create_text(101, -93, text="z", fill="black", font=('Helvetica 14 bold'))
        self.canvas.create_text(116, -110, text="1", fill="black", font=('Helvetica 14 bold'))
        self.canvas.create_polygon(110, -100, 110, -120, 90, -100)

        self.results_data = tk.Frame(self.results_frame)
        self.results_data.grid(row=0, column=1, sticky='w')
        self.results = tk.Label(self.results_data, text='', width=25, justify='left')
        self.results.grid(row=1, column=0, sticky='w')

    
    def show_enabled(self, event):
        self.section = self.selecciones.get()[0]
        self.geometric_parameters.show_entries(self.section)

    def select_calc(self, *args):
        self.calc = self.selecciones.calculo_var.get()
        self.hydraulic_parameters.change_calculation(self.calc)


    def more_info_callback(self):
        result_window = ResultsWindow(self.calculated_section.__dict__)


    def button_callback(self):
        hydraulic_params = self.hydraulic_parameters.get()
        geometric_params = self.geometric_parameters.get()
        section, calculo = self.selecciones.get()
        n_input = float(hydraulic_params['n'])
        So_input = float(hydraulic_params['So'])
        Q_input = float(hydraulic_params['Q']) if calculo != "Q" and 'Q' in  hydraulic_params else None
        y_input = float(hydraulic_params['y']) if calculo != "y" else Symbol('y')
        b_input = float(geometric_params['b']) if not geometric_params['b'].isalpha()  else None
        z_input = float(geometric_params['z']) if not geometric_params['z'].isalpha()  else None
        D_input = float(geometric_params['D']) if not geometric_params['D'].isalpha()  else None
        self.calculated_section = utils.calculate_section(section, n_input, So_input, Q_input, b_input, z_input, D_input, y_input)
        self.canvas.draw_channel(self.calculated_section.__dict__)
        self.results_title = tk.Label(self.results_data, text='Results: ', width=25, justify='left', font=("Arial", 16), anchor="w")
        self.results_title.grid(row=0, column=0, sticky='n')
        self.results.config(text = utils.formater_str(self.calculated_section.__dict__, ['n', 'So', 'Q', 'y', 'z', 'D', 'b']), font=("Arial", 12), anchor="w")
        self.more_results_button = tk.Button(self, text="More info", command=self.more_info_callback)
        self.more_results_button.grid(row=6, column=0,  padx=20, pady=0, sticky="ew" ,columnspan=2)

        self.master.geometry('670x630')


class ResultsWindow(tk.Toplevel):
    def __init__(self, section):
        super().__init__() 
        self.geometry('600x500')
        self.section = section
        
        # self.first_results = ttk.Frame(self)
        # self.first_results.grid(row=0, column=0)

        self.canvas = Canvas(self)
        self.canvas.draw_channel(section)
        self.canvas.grid(row=0, column=0)
        self.result = tk.Label(self, text=utils.formater_str(section, ['channel_type','n', 'So', 'Q', 'z', 'D', 'b']), font=("Arial", 12), anchor="w", justify='left')
        self.result.grid(row=0, column=1)
        self.result2 = tk.Label(self, text=utils.formater_str(section, ['y', 'a', 'rh', 'dh', 'tw', 'p']), font=("Arial", 12), anchor="w", justify='left')
        self.result2.grid(row=1, column=0)
        self.result3 = tk.Label(self, text=utils.formater_str(section, [ 'f', 'v', 'flow_status',  'zc', 'yn', 'Sc']), font=("Arial", 12), anchor="w", justify='left')
        self.result3.grid(row=1, column=1)

        self.print_results_button = ttk.Button(self, text='Show in Excel', command=self.open_excel)
        self.print_results_button.grid(row=2, column=0,  padx=20, pady=0, sticky="ew" ,columnspan=2)

    def open_excel(self):
        generate_report(self.section, 'OpenFlow')






