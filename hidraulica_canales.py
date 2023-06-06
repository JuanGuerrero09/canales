# Librerías
from secciones import SeccionRectangular, SeccionTrapezoidal, SeccionTriangular, SeccionCircular
from sympy import Symbol

def calcular_seccion(seccion, calculo, n_input, So_input, Q_input=None, b_input=None, z_input=None, D_input= None, y_input = Symbol('y')):
    if seccion == "Rectangular":
        # y_input = float(input("Defina la altura: "))
        seccion = SeccionRectangular(n_input, So_input, Q_input, b_input, y_input)


    elif seccion == "Triangular":
        # y_input = float(input("Defina la altura: "))
        seccion = SeccionTriangular(n_input, So_input, Q_input, z_input, y_input)

    elif seccion == "Trapezoidal":
        # y_input = float(input("Defina la altura: "))
        seccion = SeccionTrapezoidal(n_input, So_input, Q_input, b_input, z_input, y_input)

    elif seccion == "Circular":
        # y_input = float(input("Defina la altura: "))
        seccion = SeccionCircular(n_input, So_input, Q_input, D_input, y_input)

    print('vamos acá')

    if (calculo == 'yn'):
        seccion.calc_yn()

    elif(calculo == 'Q'):
        seccion.caudal_manning()

    print(seccion)
    
    return seccion

# calcular_seccion('Rectangular', 'yn', 0.013, 0.0075, 3.5, b_input=2)
# calcular_seccion('Rectangular', 'Q', 0.013, 0.0075, y_input= 0.532, b_input= 2)
# calcular_seccion('Trapezoidal', 'yn', 0.033, 0.0075, 3.5, 2, 1.5)
# calcular_seccion('Trapezoidal', 'Q', 0.033, 0.0075, y_input= 0.711, b_input= 2, z_input= 1.5)
# calcular_seccion('Triangular', 'yn', 0.033, 0.0075, 3.5, z_input=1.5)
# calcular_seccion('Triangular', 'Q', 0.033, 0.0075, y_input= 1.191, z_input= 1.5)
# calcular_seccion('Circular', 'yn', 0.013, 0.0075, 3.5, D_input=3)
# calcular_seccion('Circular', 'Q', 0.013, 0.0075, y_input= 0.608, D_input=3)




# secciones = [
#     "Cuadrada",
#     "Triangular",
#     "Trapezoidal",
#     # "Circular",
# ]

# def elegir_seccion():
    
#     opciones_seccion = [
#     inquirer.List(
#         "seccion",
#         message="Selecciona el tipo de sección a analizar",
#         choices=secciones,
#     ),
# ]
#     answers = inquirer.prompt(opciones_seccion)
#     seccion_elegida = answers["seccion"]

#     n_input = float(input("Defina el coeficiente de rugosidad: "))
#     So_input = float(input("Defina la pendiente longitudinal: "))
#     Q_input = float(input("Defina el caudal: "))


#     if seccion_elegida == "Cuadrada":
#         b_input = float(input("Defina la base: "))
#         # y_input = float(input("Defina la altura: "))
#         seccion = SeccionRectangular(n_input, So_input, Q_input, b_input)


#     elif seccion_elegida == "Triangular":
#         z_input = float(input("Defina la base: "))
#         # y_input = float(input("Defina la altura: "))
#         seccion = SeccionTriangular(n_input, So_input, Q_input, z_input)



#     elif seccion_elegida == "Trapezoidal":
#         b_input = float(input("Defina la base: "))
#         z_input = float(input("Defina la pendiente_lateral: "))
#         # y_input = float(input("Defina la altura: "))
#         seccion = SeccionTrapezoidal(n_input, So_input, Q_input, b_input, z_input)


#     # elif seccion_elegida == "Circular":
#     #     seccion = SeccionCircular()
#     #     do_input = float(input("Defina el diámetro: "))
#     #     y_input = float(input("Defina la altura: "))
#     #     seccion.set_diametro(do_input)
#     #     seccion.set_altura(y_input)

#     seccion.calc_yn()
#     return seccion.__dict__, seccion_elegida






