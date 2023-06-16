from open_flow import TrapezoidalChannel, TriangularChannel, CircularChannel, RectangularChannel
from sympy import sin, acos, sqrt
from pipe_flow import Pipe
from utils import formater_str


# Perdidas de carga h 
pipe1 = Pipe(Q=10, D=0.2, e=0.005, L=100)
print(formater_str(pipe1.__dict__, ['Q', 'D', 'a', 'e', 'eD', 'v', 'nu', 'Re', 'L', 'method', 'flow_type', 'fr', 'h', 'hf']))
# pipe1 = Pipe(Q=1, D=0.9, L=100, method='Hazen-Williams', C=140)
# print(formater_str(pipe1.__dict__, ['Q', 'D', 'a', 'v', 'nu', 'Re', 'L', 'method', 'C', 'flow_type', 'fr', 'h', 'hf']))


# print(RectangularChannel(b=2, n=0.0013, So=0.0075, Q = 3.5).__dict__)
# print(RectangularChannel(b=2, n=0.0013, So=0.0075, y = .1177).__dict__)
# print(TrapezoidalChannel(b=2, n=0.013, So=0.0075, Q = 3.5, z=1.5).__dict__)
# print(TrapezoidalChannel(b=2, n=0.013, So=0.0075, y = 0.426, z=1.5).__dict__)
# print(CircularChannel(D=1, n=0.013, So=0.0075, Q = 2.1).__dict__)
# print(CircularChannel(D=1, n=0.0013, So=0.0075, y = 0.2777).__dict__)
# print(TriangularChannel(z=1.5, n=0.0013, So=0.0075, Q = 3.5).__dict__)
# print(TriangularChannel(z=1.5, n=0.0013, So=0.0075, y = 0.354).__dict__)