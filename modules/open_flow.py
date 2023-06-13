# Imports
from sympy import Symbol, nsolve, sqrt, acos, sin, lambdify
import numpy as np 
from matplotlib import pyplot as plt 


# Variables definition

'''
https://www.eng.auburn.edu/~xzf0001/Handbook/Channels.html

'n': "Manning's Coef.",
'So': 'Channel Slope [m/m]',
'Q': 'Flow Rate [m3/s]',
'y': 'Depth [m]',
'b': 'Bottom Width [m]',
'z': 'Side Slope',
'D': 'Diameter [m]',
'a': 'Area [m2]',
'rh': 'Hydraulic Radius',
'dh': 'Hydraulic Depth',
'tw': 'Top Width [m]',
'p': 'Wetted Perimeter [m]',
'f': 'Froude Number',
'v': 'Velocity [m/s]',
'flow_status': 'Flow Status',
'zc': 'Section Factor',
'yc': 'WIP',
'vc': 'WIP',

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
        self.yn = Symbol('yn')
        self.ac = None
        self.rc = None
        self.pc = None
        self.twc = None
        self.yc = None
        self.vc = None
        self.sc = None
        
    
    def calc_properties(self):
        if self.Q is not None and type(self.y) is not Symbol:
            self.v = self.Q / self.a
            self.f = self.v / sqrt(G * self.dh)
            self.rc = self.ac / self.pc if (self.ac and self.pc) != None else None
            # self.rc = self.Q / self.ac if (self.ac) != None else None
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
    
    def get_energy(self):
        y = np.arange(0.1,4, 0.01) 
        # Crear una función evaluable a partir de la expresión self.ac
        specific_energy = lambdify(self.yn, self.yn + (self.Q**2 / (2 * G * self.ac**2)))
        # Evaluar la función en los puntos de y
        E_values = specific_energy(y)
        plt.title("Specific energy diagram") 
        plt.xlabel("Energy") 
        plt.ylabel("Depth") 
        plt.plot(E_values, y) 
        plt.show()

    def get_critical_parameters(self):
        froude_critical = (self.Q**2 / G) - (self.ac**3 / self.twc)
        self.yn = nsolve(froude_critical, self.yn, 1)
        self.yc = self.yn
        self.calc_properties()
        self.sc = ((self.Q**2 * self.n**2) / (self.ac**2 * self.rc**(4/3)))


class RectangularChannel(Channel):
    def __init__(self, n, So, b, Q = None, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.channel_type = 'Rectangular'
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
        self.twc = self.b 
        self.dh = self.y
        self.zc = self.b * (self.y**1.5)
        self.ac = self.b * self.yn
        self.pc = self.b + (self.yn * 2)
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
        self.channel_type = 'Trapezoidal'
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
        self.ac = (self.b + (self.yn*self.z)) * self.yn
        self.twc = self.b  + (2 * self.yn * self.z)
        self.pc = self.b + (2 * self.yn * (1 + self.z**2)**(1/2))
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
    
    

# channel = TrapezoidalChannel(b=2, n=0.013, So=0.0075, Q = 3.5, z=1.5)
# channel.get_energy()
# print(channel.get_critical_parameters())


class TriangularChannel(Channel):
    def __init__(self, n, So, z, Q = None, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.channel_type = 'Triangular'
        self.z = z
        self.y = y
        if(type(self.y) is Symbol):
            self.calc_yn()
        if(self.Q is None):
            self.calc_flow()

    def calc_properties(self):
        self.a = self.z * self.y**2
        self.an = self.z * self.yn**2
        self.p = (self.y * 2) * (1 + self.z**2)**0.5
        self.rh = self.a / self.p
        self.tw = 2 * self.z * self.y
        self.dh = 0.5 * self.y
        self.ac = self.z * self.yn**2
        self.twc = 2 * self.z * self.yn
        self.pc = (self.yn * 2) * (1 + self.z**2)**0.5
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
        self.channel_type = 'Circular'
        self.D = D
        self.y = y
        if(type(self.y) is Symbol):
            self.calc_yn()
        if(self.Q is None):
            self.calc_flow()


    def calc_properties(self):
        self.theta_n = acos((1 - ( 2 * (self.yn / self.D)))) * 2
        self.theta = acos((1 - ( 2 * (self.y / self.D)))) * 2
        self.a = ((self.theta - sin(self.theta)) * self.D**2) / 8
        self.ac = ((self.theta_n - sin(self.theta_n)) * self.D**2) / 8
        self.a = ((self.theta - sin(self.theta)) * self.D**2) / 8
        self.p = ( self.D * self.theta) / 2
        self.rh = self.a / self.p
        self.tw = sin(self.theta / 2) * self.D
        self.twc = sin(self.theta_n / 2) * self.D
        self.pc = ( self.D * self.theta_n) / 2
        self.dh = self.a / self.tw
        self.zc = self.D * (self.y**1.5)
        super().calc_properties()
        

    def __str__(self):
        return f"\nChannel: {self.channel_type}\nDimensions: \n\tDiameter: {self.D}\n{super().__str__()}"
    
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
