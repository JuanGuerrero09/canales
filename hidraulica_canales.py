# Librerías
import pprint
import inquirer
from secciones import SeccionRectangular, SeccionTrapezoidal, SeccionTriangular



# class SeccionCircular:
#     def __init__(self):
#         self.do = None
#         self.y = None

#     def set_diametro(self, value):
#         self.do = value

#     def set_altura(self, value):
#         self.y = value

#     def set_area(self):
#         self.area = self.b * self.y

#     def set_perimetro_mojado(self):
#         self.perimetro_mojado = self.b + (self.y * 2)

#     def set_radio_hidraulico(self):
#         self.radio_hidraulico = self.area / self.perimetro_mojado

#     def set_ancho_superficial(self):
#         self.ancho_superficial = self.b 

#     def set_profundidad_hidraulica(self):
#         self.profundidad_hidraulica = self.y

#     def set_factor_de_seccion(self):
#         self.factor_de_seccion = self.b * (self.y**1.5)

secciones = [
    "Cuadrada",
    "Triangular",
    "Trapezoidal",
    # "Circular",
]

def elegir_seccion():
    
    opciones_seccion = [
    inquirer.List(
        "seccion",
        message="Selecciona el tipo de sección a analizar",
        choices=secciones,
    ),
]
    answers = inquirer.prompt(opciones_seccion)
    seccion_elegida = answers["seccion"]

    n_input = float(input("Defina el coeficiente de rugosidad: "))
    So_input = float(input("Defina la pendiente longitudinal: "))
    Q_input = float(input("Defina el caudal: "))


    if seccion_elegida == "Cuadrada":
        b_input = float(input("Defina la base: "))
        # y_input = float(input("Defina la altura: "))
        seccion = SeccionRectangular(n_input, So_input, Q_input, b_input)


    elif seccion_elegida == "Triangular":
        z_input = float(input("Defina la base: "))
        # y_input = float(input("Defina la altura: "))
        seccion = SeccionTriangular(n_input, So_input, Q_input, z_input)



    elif seccion_elegida == "Trapezoidal":
        b_input = float(input("Defina la base: "))
        z_input = float(input("Defina la pendiente_lateral: "))
        # y_input = float(input("Defina la altura: "))
        seccion = SeccionTrapezoidal(n_input, So_input, Q_input, b_input, z_input)


    # elif seccion_elegida == "Circular":
    #     seccion = SeccionCircular()
    #     do_input = float(input("Defina el diámetro: "))
    #     y_input = float(input("Defina la altura: "))
    #     seccion.set_diametro(do_input)
    #     seccion.set_altura(y_input)

    seccion.calc_yn()
    return seccion.__dict__, seccion_elegida

# def calculo_de_elementos_geometricos(seccion):
#     seccion_elegida = seccion["tipo de sección"]
#     if seccion_elegida == "Cuadrada":
#         A = seccion['b']*seccion['']
#     elif seccion_elegida == "Triangular":
#     elif seccion_elegida == "Trapezoidal":
#     elif seccion_elegida == "Circular":

seccion = elegir_seccion()






