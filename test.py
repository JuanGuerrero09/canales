from open_flow import TrapezoidalChannel, TriangularChannel, CircularChannel, RectangularChannel


print('Primer canal')
canal1 = TrapezoidalChannel(0.013, 0.0075, z=1.5, b=2, Q=3.5)
canal1.get_critical_parameters()
print(canal1.__dict__)
print('Segundo canal')
canal1 = TriangularChannel(0.013, 0.0075, z=1.5, Q=3.5)
canal1.get_critical_parameters()
print(canal1.__dict__)
print('Tercer canal')
canal1 = CircularChannel(0.013, 0.0075, D=3, Q=3.5)
canal1.get_critical_parameters()
print(canal1.__dict__)
print('Cuarto canal')
canal1 = RectangularChannel(0.013, 0.0075, b=2, Q=3.5)
canal1.get_critical_parameters()
print(canal1.__dict__)