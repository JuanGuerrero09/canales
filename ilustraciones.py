import turtle
import tkinter as tk
from math import sqrt, atan, degrees, sin, cos, radians


def draw_trapezoidal_channel(yn, b, z, turtle_screen):

    # Dibujar el canal trapezoidal
    factor = 300 / (b + (2 * (yn + 0.3) *z))

    side_slope = z if z < 5 else 5
    if (yn + 0.3) * factor > 160:
        factor = 160 / (yn + 0.3)
    elif (yn + 0.3) * factor < 40:
        factor = 40 / (yn + 0.3)
    channel_depth = (yn + 0.3) * factor
    yn = yn * factor 
    angle = degrees(atan(1 / side_slope))
    base_width = b * factor if b * factor < 120 else 120

    top_width = base_width + 2 * (channel_depth * side_slope)
    yn_top_width = base_width + 2 * (yn * side_slope) 
    diagonal_length = channel_depth * sqrt(1 + side_slope**2)
    yn_diagonal_length = yn * sqrt(1 + side_slope**2)

    print(channel_depth, top_width, factor)

    turtle_obj = turtle.RawTurtle(turtle_screen)
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

    turtle_screen.update()

# Llamar a la función para dibujar el canal trapezoidal
# draw_trapezoidal_channel(z=1.5, b=2, yn=0.542, trutle_screen=turtle_screen)

def draw_rectangular(yn, b, turtle_screen):

    # Dibujar el canal trapezoidal
    factor = 200 / b 
    print(factor)
    base_width = b * factor
    if (yn + 0.3) * factor > 170:
        factor = 170 / (yn + 0.3)
    elif (yn + 0.3) * factor < 40:
        factor = 40 / (yn + 0.3)
    height = (yn + 0.3) * factor
    print(height)
    yn = yn * factor


    turtle_obj = turtle.RawTurtle(turtle_screen)
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

    turtle_screen.update()

def draw_triangle(z, yn, turtle_screen):
    # Dibujar el canal triangular

    factor = 200 / (2 * yn * z)
    print(factor)
    if (yn + 0.2) * factor > 170:
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

    turtle_obj = turtle.RawTurtle(turtle_screen)
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

    turtle_screen.update()




def draw_circle(diameter, angle, turtle_screen):

    diameter = 200
    # Configuración inicial de Turtle
    turtle_obj = turtle.RawTurtle(turtle_screen)
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

    turtle_screen.update()



