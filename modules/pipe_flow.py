import fluids

from math import pi
#Constants

G = 9.81 #gravity
nu_20c = 0.0000010533 #kinematic viscosity at 20 C

class Pipe:
    def __init__(self, Q, D, e, L= None, n=None, rho = None, mu = None, nu = None, C = None, method= 'Darcy-Weisbach'):
        self.Q = Q
        self.D = D
        self.e = e
        self.eD = self.e / self.D
        self.v = Q / (pi * D**2 /4)
        self.nu = rho / mu if (rho and mu) != None else nu_20c
        self.Re = self.v * self.D / self.nu
        self.method = method
        self.C = C
        if(self.Re < 2000):
            self.flow_type = 'Laminar flow'
            self.f = 64 / self.Re
        elif (self.Re < 4000):
            self.flow_type = 'Transitional flow'
            self.f = self.calc_friction()
        elif (self.Re >= 4000):
            self.flow_type = 'Turbulent flow'
            self.f = self.calc_friction()
        self.h = self.calc_head_loss()

    def calc_friction(self):
        f = fluids.friction_factor(self.Re, self.eD)
        return f
    def calc_head_loss(self):
        match self.method:
            case 'Darcy-Weisbach':
                h = self.f * self.v**2 / (2 * self.D * G)
                return h
            case 'Hazen-Williams':
                h = 10.674 * self.Q**1.852 / (self.D**4.78 * self.C**1.852)
                return h

pipe1 = Pipe(1, 0.2, 0.0015, method='Hazen-Williams', C=150)
print(pipe1.__dict__)
        

# Perdidas de carga h 

"""
Q-> Caudal
D-> Diametro interno
e -> coef rugosidad del material
Darcy (f, L?, D, Q, g)
Manning (n, D, Q, L)
Hazen-Williams (Q, C, D, L)

f -> v, D, rho, mu(viscosidad dinamica), e (Darcy) Re (rho (densidad), v, D, mu (viscocidad cinematica 0.1))
C -> D, f
eD -> e/D

"""

# print(fluids.friction_factor(Re=52222, eD=0.0001/0.5))