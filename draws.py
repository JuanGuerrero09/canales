import turtle
from svg_turtle import SvgTurtle
import tkinter as tk
from math import sqrt, atan, degrees, sin, cos, radians
import cairosvg




def get_img_from_draw(channel: SvgTurtle):

    channel.save_as('channel.svg')
    # Ruta del archivo SVG de entrada
    input_file = 'channel.svg'

    # Ruta del archivo PNG de salida
    output_file = "channel.png"

    # Convertir SVG a PNG
    cairosvg.svg2png(url=input_file, write_to=output_file, background_color="white")
    


def draw_Trapezoid_channel(yn, b, z):

    # Dibujar el canal Trapezoid
    factor = 250 / (b + (2 * (yn + 0.3) *z))

    side_slope = z if z < 5 else 5
    if (yn + 0.3) * factor > 130:
        factor = 130 / (yn + 0.3)
    elif (yn + 0.3) * factor < 40:
        factor = 40 / (yn + 0.3)
    channel_depth = (yn + 0.3) * factor
    yn = yn * factor 
    angle = degrees(atan(1 / side_slope))
    base_width = b * factor if b * factor < 105 else 105

    top_width = base_width + 2 * (channel_depth * side_slope)
    yn_top_width = base_width + 2 * (yn * side_slope) 
    diagonal_length = channel_depth * sqrt(1 + side_slope**2)
    yn_diagonal_length = yn * sqrt(1 + side_slope**2)


    turtle_obj = SvgTurtle(300, 300)
    turtle_obj.hideturtle()
    turtle_obj.hideturtle()
    turtle_obj.penup()
    turtle_obj.goto(0, -50)
    turtle_obj.pendown()
    turtle_obj.pensize(3)

    turtle_obj.forward(base_width/2)
    turtle_obj.left(angle)
    turtle_obj.forward(diagonal_length)
    turtle_obj.left(180 - angle)
    turtle_obj.penup()
    turtle_obj.forward(top_width)
    turtle_obj.pendown()
    turtle_obj.left(180 - angle)
    turtle_obj.forward(diagonal_length)
    turtle_obj.left(angle)
    turtle_obj.forward(base_width/2)



    turtle_obj.fillcolor('blue')
    turtle_obj.begin_fill()
    turtle_obj.forward(base_width/2)
    turtle_obj.left(angle)
    turtle_obj.forward(yn_diagonal_length)
    turtle_obj.left(180 - angle)
    turtle_obj.pensize(1)
    turtle_obj.forward(yn_top_width)
    turtle_obj.pensize(3)
    turtle_obj.left(180 - angle)
    turtle_obj.forward(yn_diagonal_length)
    turtle_obj.left(angle)
    turtle_obj.forward(base_width/2)
    turtle_obj.end_fill()

    return turtle_obj

# Llamar a la función para dibujar el canal Trapezoid
# draw_Trapezoid_channel(z=1.5, b=2, yn=0.542, trutle_screen=turtle_screen)

def draw_Rectangle(yn, b):

    # Dibujar el canal Trapezoid
    factor = 170 / b 
    base_width = b * factor
    if (yn + 0.3) * factor > 150:
        factor = 150 / (yn + 0.3)
    elif (yn + 0.3) * factor < 40:
        factor = 40 / (yn + 0.3)
    height = (yn + 0.3) * factor
    yn = yn * factor


    turtle_obj = SvgTurtle(300, 300)
    turtle_obj.hideturtle()
    turtle_obj.penup()
    turtle_obj.goto(0, -50)
    turtle_obj.pendown()

    turtle_obj.forward(base_width/2)
    turtle_obj.left(90)
    turtle_obj.forward(height)
    turtle_obj.left(90)
    turtle_obj.penup()
    turtle_obj.forward(base_width)
    turtle_obj.pendown()
    turtle_obj.left(90)
    turtle_obj.forward(height)
    turtle_obj.left(90)
    turtle_obj.forward(base_width/2)



    turtle_obj.fillcolor('blue')
    turtle_obj.begin_fill()
    turtle_obj.forward(base_width/2)
    turtle_obj.left(90)
    turtle_obj.forward(yn)
    turtle_obj.left(90)
    turtle_obj.forward(base_width)
    turtle_obj.left(90)
    turtle_obj.forward(yn)
    turtle_obj.left(90)
    turtle_obj.forward(base_width/2)
    turtle_obj.end_fill()
    return turtle_obj


def draw_triangle(z, yn):
    # Dibujar el canal Triangle

    factor = 180 / (2 * yn * z)
    if (yn + 0.2) * factor > 150:
        factor = 170 / (yn + 0.3)
    elif (yn + 0.3) * factor < 100:
        factor = 100 / (yn + 0.3)

    channel_depth = (yn + 0.2) * factor
    yn = yn * factor
    side_slope = z if z < 1.5 else 1.5
    angle = degrees(atan(1 / side_slope))

    top_width =  2 * (channel_depth * side_slope)
    yn_top_width = 2 * (yn * side_slope)
    diagonal_length = channel_depth * sqrt(1 + side_slope**2)
    yn_diagonal_length = yn * sqrt(1 + side_slope**2)

    turtle_obj = SvgTurtle(300, 300)
    turtle_obj.hideturtle()
    turtle_obj.hideturtle()
    turtle_obj.penup()
    turtle_obj.goto(0, -80)
    turtle_obj.pendown()

    turtle_obj.left(angle)
    turtle_obj.forward(diagonal_length)
    turtle_obj.left(180 - angle)
    turtle_obj.penup()
    turtle_obj.forward(top_width)
    turtle_obj.pendown()
    turtle_obj.left(180 - angle)
    turtle_obj.forward(diagonal_length)

    turtle_obj.fillcolor('blue')
    turtle_obj.begin_fill()

    turtle_obj.left(2 * angle)
    turtle_obj.forward(yn_diagonal_length)
    turtle_obj.left(180 - angle)
    turtle_obj.forward(yn_top_width)
    turtle_obj.left(180 - angle)
    turtle_obj.forward(yn_diagonal_length)
    turtle_obj.end_fill()
    return turtle_obj





def draw_circle(diameter, angle):

    diameter = 180
    # Configuración inicial de Turtle
    turtle_obj = SvgTurtle(300, 300)
    turtle_obj.speed(100)
    turtle_obj.hideturtle() 
    turtle_obj.penup()
    turtle_obj.goto(-sin(radians(angle/2))*diameter/2,-cos(radians(angle/2))* diameter/2)
    turtle_obj.pendown()

    # Dibujar el círculo
    turtle_obj.left(-angle/2)
    turtle_obj.circle(diameter/2)


    # Dibujar el semicírculo
    turtle_obj.fillcolor('blue')
    turtle_obj.begin_fill()
    turtle_obj.circle(diameter/2, angle)
    turtle_obj.end_fill()

    # Finalizar el dibujo
    turtle_obj.pendown()

    return turtle_obj



