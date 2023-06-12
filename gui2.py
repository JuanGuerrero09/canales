from svg_turtle import SvgTurtle
import turtle
import tkinter as tk
from math import sqrt, atan, degrees, sin, cos, radians

b = 2
yn = 0.432
z = 1.5
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

print(channel_depth, top_width, factor)

turtle_obj = SvgTurtle(550, 550)
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

print(type(turtle_obj))

turtle_obj.save_as('example.svg')