import turtle
import tkinter as tk
from math import sqrt, atan, degrees, sin, cos, radians
def draw_trapezoidal_channel(yn, b, z, turtle_screen):

    # Dibujar el canal trapezoidal
    base_width = b * 100
    side_slope = z
    channel_depth = (yn + 0.2) * 100
    yn = yn * 100
    angle = degrees(atan(1 / side_slope))

    top_width = base_width + 2 * (channel_depth * side_slope)
    yn_top_width = base_width + 2 * (yn * side_slope)
    diagonal_length = channel_depth * sqrt(1 + side_slope**2)
    yn_diagonal_length = yn * sqrt(1 + side_slope**2)

    turtle_obj = turtle.RawTurtle(turtle_screen)
    turtle_obj.hideturtle()
    turtle_obj.hideturtle()
    turtle_obj.penup()
    turtle_obj.goto(0, -50)
    turtle_obj.pendown()

    turtle_obj.forward(base_width/2)
    turtle_obj.left(angle)
    turtle_obj.forward(diagonal_length)
    turtle_obj.left(180 - angle)
    turtle_obj.forward(top_width)
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
    turtle_obj.forward(yn_top_width)
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
    base_width = b * 100
    height = (yn + 0.3) * 100
    yn = yn * 100


    turtle_obj = turtle.RawTurtle(turtle_screen)
    turtle_obj.hideturtle()
    turtle_obj.penup()
    turtle_obj.goto(0, -50)
    turtle_obj.pendown()

    turtle_obj.forward(base_width/2)
    turtle_obj.left(90)
    turtle_obj.forward(height)
    turtle_obj.left(90)
    turtle_obj.forward(base_width)
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
    channel_depth = (yn + 0.2) * 100
    yn = yn * 100
    side_slope = z
    angle = degrees(atan(1 / side_slope))

    top_width =  2 * (channel_depth * side_slope)
    yn_top_width = 2 * (yn * side_slope)
    diagonal_length = channel_depth * sqrt(1 + 0.5**2)
    yn_diagonal_length = yn * sqrt(1 + 0.5**2)

    turtle_obj = turtle.RawTurtle(turtle_screen)
    turtle_obj.hideturtle()
    turtle_obj.hideturtle()
    turtle_obj.penup()
    turtle_obj.goto(0, -80)
    turtle_obj.pendown()

    turtle_obj.left(angle)
    turtle_obj.forward(diagonal_length)
    turtle_obj.left(180 - angle)
    turtle_obj.forward(top_width)
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

    diameter = diameter * 100
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



