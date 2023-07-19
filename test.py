from open_flow import TrapezoidalChannel, TriangularChannel, CircularChannel, RectangularChannel
# from pipe_flow import Pipe

# # Calculate friction losses in a pipe

# #Example with Darcy (default)
# pipe1 = Pipe(Q=10, D=0.2, e=0.005, L=100)
# print(pipe1.__dict__)
# #Example with azen-Williams
# pipe2 = Pipe(Q=1, D=0.9, L=100, method='Hazen-Williams', C=140)
# print(pipe2.__dict__)

# # Calculate depth in an open channel
# print(RectangularChannel(b=2, n=0.0013, So=0.0075, Q = 3.5).__dict__)
# print(TrapezoidalChannel(b=2, n=0.013, So=0.0075, Q = 3.5, z=1.5).__dict__)
# print(CircularChannel(D=1, n=0.013, So=0.0075, Q = 2.1).__dict__)
# print(TriangularChannel(z=1.5, n=0.0013, So=0.0075, Q = 3.5).__dict__)

# # Calculate flow rate in an open channel using Manning's equation
# print(RectangularChannel(b=2, n=0.0013, So=0.0075, y = .1177).__dict__)
# print(TrapezoidalChannel(b=2, n=0.013, So=0.0075, y = 0.426, z=1.5).__dict__)
# print(CircularChannel(D=1, n=0.0013, So=0.0075, y = 0.2777).__dict__)
# print(TriangularChannel(z=1.5, n=0.0013, So=0.0075, y = 0.354).__dict__)

# print(RectangularChannel(b=50, n=0.015, So=0.02, y = 15).__dict__)