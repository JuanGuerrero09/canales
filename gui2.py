import tkinter as tk
from tkinter import ttk
from hidraulica_canales import calcular_seccion
import turtle
from math import sqrt, atan, degrees, radians
from ilustraciones import draw_Trapezoid_channel, draw_circle, draw_triangle, draw_Rectangle
from custom_components import CustomEntry


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
            case 'Trapezoid':
                draw_Trapezoid_channel(yn=yn, z=z, b=b, turtle_screen=self.get_turtle_screen())
            case 'Circle':
                draw_circle(diameter=diameter, angle=angle, turtle_screen=self.get_turtle_screen())
            case 'Rectangle':
                draw_Rectangle(yn=yn, b=b, turtle_screen=self.get_turtle_screen())
            case 'Triangle':
                draw_triangle(yn=yn, z=z,turtle_screen=self.get_turtle_screen())


seccion_calculada = {'n': 0.013, 'So': 0.0075, 'Q': 3.5, 'y': 0.426774293412530, 'area': 1.12675303310171, 'perimetro_mojado': 3.53875659794879, 'radio_hidraulico': 0.318403654479887, 'ancho_superficial': 3.28032288023759, 'profundidad_hidraulica': 0.343488453496412, 'factor_de_seccion': 0.621192378388255, 'velocidad': 3.10627075958718, 'froude': 1.51811852160482, 'tipo_de_flujo': 'Supercritical', 'tipo_canal': 'Trapezoid', 'b': 2.0, 'z': 1.5}


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hydrosolve")
        self.geometry("650x550")
        self.grid_columnconfigure((0, 1), weight=1)

        self.title_label = tk.Label(self, text='Hydrosolve', justify='center', height=2, font=('Helvetica 16 bold'))
        self.title_label.grid(row=0, columnspan=2)
        result_window = ResultsWindow(seccion_calculada)
        
class ResultsWindow(tk.Toplevel):
    def __init__(self, section):
        super().__init__()  # Corrected super() call
        self.geometry('600x600')
        self.result = tk.Label(self, text=section)
        self.result.grid(row=0, column=1)
        self.canvas = Canvas(self)
        print(section.__dict__)
        self.canvas.draw_channel(section.__dict__)
        self.canvas.grid(row=0, column=0)


    # def get_picture(self):
    #     self.canvas.update_idletasks()
    #     x = self.canvas.winfo_rootx() 
    #     y = self.canvas.winfo_rooty() 
    #     width = self.canvas.winfo_width() 
    #     height = self.canvas.winfo_height() 
    #     # x = self.canvas.winfo_rootx() + 52
    #     # y = self.canvas.winfo_rooty() + 110
    #     # width = self.canvas.winfo_width() + 50
    #     # height = self.canvas.winfo_height() + 20

    #     # Capturar la imagen del canvas utilizando ImageGrab
    #     image = ImageGrab.grab((x, y, x + width, y + height))
    #     print('x1: ', x, y, 'x2', x + width, y + height)
    #     image.save('canvas_image.png')
    #     image.show()




section = calcular_seccion('Trapezoid', 'yn', 0.012, 0.0075, 3.5, 2, 1.5)
print(section)
app2 = ResultsWindow(section)
app2.mainloop()