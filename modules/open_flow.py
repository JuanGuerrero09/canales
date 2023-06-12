# Imports
from sympy import Symbol, nsolve, sqrt, acos, sin



# Variables definition

'''
https://www.eng.auburn.edu/~xzf0001/Handbook/Channels.html
n = n
So = Channel slope
Q = Q
y = None
a = None
wetted_perimeter = None
rh = None
tw = None
dh = None
zc = None
velocidad = None
froude = None
tipo_de_flujo = None
Top width
Flow a
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
        # self.yn = Symbol('yn')
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
        print(self.rh)
        self.Q = (self.a * self.rh**(2/3) * self.So**0.5) / self.n
        self.calc_properties()
        return self.Q

    def calc_yn(self):
        if(type(self.y) is Symbol):
            self.calc_properties()
            sol = (self.a * self.rh**(2/3) * self.So**0.5) / self.n
            self.y = nsolve(sol - self.Q, self.y, 1)
            self.calc_properties()
        return self.y

    def get_parameters(self):
        return self.__dict__


class RectangularChannel(Channel):
    def __init__(self, n, So, b, Q = None, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.b = b
        self.y = y
        if(type(self.y) is Symbol):
            self.calc_yn()
        if(self.Q is None):
            self.calc_flow()

    def calc_properties(self):
        self.a = self.b * self.y
        self.p = self.b + (self.y * 2)
        self.rh = self.a / self.p
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
    def __init__(self, n, So, z, b, Q = None, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.b = b
        self.z = z
        self.y = y
        if(type(self.y) is Symbol):
            self.calc_yn()
        if(self.Q is None):
            self.calc_flow()

    def calc_properties(self):
        self.a = (self.b + (self.y*self.z)) * self.y
        self.p = self.b + (2 * self.y * (1 + self.z**2)**(1/2))
        self.rh = self.a / self.p
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
    def __init__(self, n, So, z, Q = None, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.tipo_canal = 'Triangle'
        self.z = z
        self.y = y
        if(type(self.y) is Symbol):
            self.calc_yn()
        if(self.Q is None):
            self.calc_flow()

    def calc_properties(self):
        self.a = self.z * self.y**2
        self.p = (self.y * 2) * (1 + self.z**2)**0.5
        self.rh = self.a / self.p
        self.tw = 2 * self.z * self.y
        self.dh = 0.5 * self.y
        self.zc = ((2**0.5)/2) * self.z * self.y**2.5
        super().calc_properties()

    def caudal_manning(self):
        self.calc_properties()
        self.Q = (self.a * self.rh**(2/3) * self.So**0.5) / self.n
        self.calc_properties()    
    
    def calc_yn(self):
        if isinstance(self.y, Symbol):
            self.calc_properties()
            sol = (self.a * self.rh**(2/3) * self.So**0.5) / self.n
            self.y = nsolve(sol - self.Q, self.y, 1)  # Pasar self.y como variable simbólica
            self.calc_properties()
        else:
            self.calc_properties()
        return self.y

class CircularChannel(Channel):
    def __init__(self, n, So, D, Q = None, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.tipo_canal = 'Circle'
        self.D = D
        self.y = y
        self.theta = acos((1 - ( 2 * (self.y / self.D)))) * 2
        if(type(self.y) is Symbol):
            self.calc_yn()
        if(self.Q is None):
            self.calc_flow()


    def calc_properties(self):
        self.theta = acos((1 - ( 2 * (self.y / self.D)))) * 2
        self.a = ((self.theta - sin(self.theta)) * self.D**2) / 8
        self.p = ( self.D * self.theta) / 2
        self.rh = self.a / self.p
        self.tw = sin(self.theta / 2) * self.D
        # self.dh = self.y
        # self.zc = self.D * (self.y**1.5)
        super().calc_properties()
        

    def __str__(self):
        return f"\nChannel: {self.tipo_canal}\nDimensions: \n\tDiameter: {self.D}\n{super().__str__()}"
    
    def caudal_manning(self):
        self.calc_properties()
        self.Q = (self.a * self.rh**(2/3) * self.So**0.5) / self.n
        self.calc_properties()

    
    def calc_yn(self):
        if isinstance(self.y, Symbol):
            self.calc_properties()
            sol = (self.a * self.rh**(2/3) * self.So**0.5) / self.n
            self.y = nsolve(sol - self.Q, self.y, 1)  # Pasar self.y como variable simbólica
            self.calc_properties()
        else:
            self.calc_properties()
        return self.y

# print(RectangularChannel(b=2, n=0.0013, So=0.0075, Q = 3.5).__dict__)
# print(RectangularChannel(b=2, n=0.0013, So=0.0075, y = .1177).__dict__)
# print(TrapezoidalChannel(b=2, n=0.013, So=0.0075, Q = 3.5, z=1.5).__dict__)
# print(TrapezoidalChannel(b=2, n=0.013, So=0.0075, y = 0.426, z=1.5).__dict__)
# print(CircularChannel(D=3, n=0.0013, So=0.0075, Q = 3.5).__dict__)
# print(CircularChannel(D=3, n=0.0013, So=0.0075, y = 0.2015).__dict__)
# print(TriangularChannel(z=1.5, n=0.0013, So=0.0075, Q = 3.5).__dict__)
# print(TriangularChannel(z=1.5, n=0.0013, So=0.0075, y = 0.354).__dict__)