from sympy import symbols, sqrt, nsolve, acos, sin
from math import  pi


b = 2.35
z = 1.5
So = 0.0075
n = 0.013
y = symbols('y')

# Función objetivo
def f(y):
    return (((b + (y*z)) * y) * (((b + (y*z)) * y)/(b + (2 * y * sqrt(1 + z**2))))**(2/3) * (So)**0.5) / (n) - 3.5

# Método de la secante
def secante(f, x0=0, x1=30, tol=1e-6, max_iter=100):
    i = 0
    while abs(x1 - x0) > tol and i < max_iter:
        x0, x1 = x1, x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        i += 1
    return x1

# Calcula la aproximación de la solución
y_approx = secante(f, 0.3, 0.4)  # Puedes ajustar los valores iniciales según tus necesidades



print(nsolve(f(y), 3.5))


D = 3
Q = 3.5

from sympy import Symbol, nsolve
x1 = Symbol('x1')
x2 = Symbol('x2')
f1 = 3 * x1**2 - 2 * x2**2 - 1
f2 = x1**2 - 2 * x1 + x2**2 + 2 * x2 - 8
print(nsolve((f1, f2), (x1, x2), (-1, 1)))

# theta = Symbol('thetha')
d = symbols('d')
# d = 0.6083
thetasolved = 1.868388

theta =  acos((1 - ( 2 * (d / D)))) * 2

def area(theta):
    return ((theta - sin(theta)) * D**2) / 8

def perimetro_mojado(theta):
    return ( D * theta) / 2

def radio_hidraulico(theta):
    return area(theta) / perimetro_mojado(theta)

def caudal_manning(d):
    theta =  acos((1 - ( 2 * (d / D)))) * 2
    return (area(theta) * radio_hidraulico(theta)**(2/3) * So**0.5) / n


print(nsolve(caudal_manning(d) - Q, d, 1))

# print(nsolve((angulo_central, caudal_manning), (d, theta), (0, 3.5)))
# print(caudal_manning(d))


def theta_prueba(d):
    return acos((1 - (2 * (d / 3.5)))) * 2

d = Symbol('d')
sol = nsolve(theta_prueba(d) - 1.868388, d, 1)  # Puedes ajustar el valor inicial de 'd' según sea necesario
print(sol)