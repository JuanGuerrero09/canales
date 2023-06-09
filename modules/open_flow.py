# Imports
from sympy import Symbol, nsolve, sqrt



# Variables definition

'''
https://www.eng.auburn.edu/~xzf0001/Handbook/Channels.html
n = n
So = Channel slope
Q = Q
y = None
area = None
wetted_perimeter = None
radio_hidraulico = None
ancho_superficial = None
profundidad_hidraulica = None
factor_de_seccion = None
velocidad = None
froude = None
tipo_de_flujo = None
Top width
Flow Area
Section Factor
Critical depth
Critical slope
Flow status
Specific Energy
Froude Number
'''

# Constants

G = 9.81 #acceleration due gravity

# Classes

class Channel:
    def __init__(self, n, So, Q):
        self.n = n
        self.So = So
        self.Q = Q
        self.y = None
        self.a = None
        self.p = None
        self.rh = None
        self.tw = None
        self.dh = None
        self.zc = None
        self.v = None
        self.f = None
        self.flow_status = None
        self.yc = None
        self.vc = None
    
    def calc_properties(self):
        if self.Q is not None and type(self.y) is not Symbol:
            self.v = self.Q / self.a
            self.f = self.v / sqrt(G * self.y)
            froude_value = float(str(self.f))
            if froude_value > 1.0:
                self.flow_status = 'Supercritical'
            elif froude_value == 1.0:
                self.flow_status = 'Critical'
            else:
                self.flow_status = 'Subcritical'
        else:
            pass

    def calc_flow(self):
        #Manning
        self.calc_properties()
        self.Q = (self.a * self.rh**(2/3) * self.So**0.5) / self.n
        self.calc_properties()
        return self.Q

    def get_parameters(self):
        return self.__dict__


class RectangularChannel(Channel):
    def __init__(self, n, So, Q, b, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.b = b
        self.y = y

    def calc_properties(self):
        self.a = self.b * self.y
        self.p = self.b + (self.y * 2)
        self.rh = self.area / self.perimetro_mojado
        self.tw = self.b 
        self.dh = self.y
        self.zc = self.b * (self.y**1.5)
        super().calc_properties()

    def calc_yn(self):
        if(type(self.y) is Symbol):
            self.calc_properties()
            sol = (self.a * self.rh**(2/3) * self.So**0.5) / self.n
            self.y = nsolve(sol - self.Q, self.y, 1)
            self.calc_properties()
        return self.y
    
    
class TrapezoidalChannel(Channel):
    def __init__(self, n, So, Q, b, z, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.b = b
        self.z = z
        self.y = y

    def calc_propiedades(self):
        self.area = (self.b + (self.y*self.z)) * self.y
        self.p = self.b + (2 * self.y * (1 + self.z**2)**(1/2))
        self.rh = self.area / self.perimetro_mojado
        self.tw = self.b  + (2 * self.y * self.z)
        self.dh = ((self.b + (self.z * self.y))* self.y) / (self.b + (2 * self.z * self.y))
        self.zc = ((self.b + (self.z * self.y))* self.y)**1.5 / (self.b + (2 * self.y * self.b))**0.5
        super().calc_properties()

    def calc_yn(self):
        if isinstance(self.y, Symbol):
            self.calc_properties()
            sol = (self.a * self.rh**(2/3) * self.So**0.5) / self.n
            self.y = nsolve(sol - self.Q, self.y, 1) 
            self.calc_properties()
        else: 
            self.calc_properties()
        return self.y

class TriangularChannel(Channel):
    def __init__(self, n, So, Q, z, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.tipo_canal = 'Triangle'
        self.z = z
        self.y = y

    def calc_propiedades(self):
        self.area = self.z * self.y**2
        self.perimetro_mojado = (self.y * 2) * (1 + self.z**2)**0.5
        self.radio_hidraulico = self.area / self.perimetro_mojado
        self.ancho_superficial = 2 * self.z * self.y
        self.profundidad_hidraulica = 0.5 * self.y
        self.factor_de_seccion = ((2**0.5)/2) * self.z * self.y**2.5
        super().calc_propiedades()

    def caudal_manning(self):
        self.calc_propiedades()
        self.Q = (self.area * self.radio_hidraulico**(2/3) * self.So**0.5) / self.n
        self.calc_propiedades()    
    
    def calc_yn(self):
        if(type(self.y) is Symbol):
            self.calc_propiedades()
            self.y = solve(((self.area * self.radio_hidraulico**(2/3) * self.So**0.5) / self.n) - self.Q, self.y)[0]
            self.calc_propiedades()
        else: 
            self.calc_propiedades()

class CircularChannel(Channel):
    def __init__(self, n, So, Q, D, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.tipo_canal = 'Circle'
        self.D = D
        self.y = y
        self.theta = acos((1 - ( 2 * (self.y / self.D)))) * 2


    def calc_propiedades(self):
        self.theta = acos((1 - ( 2 * (self.y / self.D)))) * 2
        self.area = ((self.theta - sin(self.theta)) * self.D**2) / 8
        self.perimetro_mojado = ( self.D * self.theta) / 2
        self.radio_hidraulico = self.area / self.perimetro_mojado
        self.ancho_superficial = sin(self.theta / 2) * self.D
        # self.profundidad_hidraulica = self.y
        # self.factor_de_seccion = self.D * (self.y**1.5)
        super().calc_propiedades()
        

    def __str__(self):
        return f"\nChannel: {self.tipo_canal}\nDimensions: \n\tDiameter: {self.D}\n{super().__str__()}"
    
    def caudal_manning(self):
        self.calc_propiedades()
        self.Q = (self.area * self.radio_hidraulico**(2/3) * self.So**0.5) / self.n
        self.calc_propiedades()

    
    def calc_yn(self):
        if isinstance(self.y, Symbol):
            self.calc_propiedades()
            sol = (self.area * self.radio_hidraulico**(2/3) * self.So**0.5) / self.n
            self.y = nsolve(sol - self.Q, self.y, 1)  # Pasar self.y como variable simbólica
            self.calc_propiedades()
        else:
            self.calc_propiedades()
        return self.y

