import fluids

from math import pi
#Constants

G = 9.81 #gravity
nu_20c = 0.0000010533 #kinematic viscosity at 20 C

class Pipe:
    def __init__(self, Q, D, e= None, L= None, rho = None, mu = None, C = None, method= 'Darcy-Weisbach'):
        self.Q = Q
        self.D = D
        self.a = self.D**2 * pi / 4
        self.e = e
        self.eD = self.e / self.D if (e and D) != None else None
        self.v = Q / (pi * D**2 /4)
        self.nu = rho / mu if (rho and mu) != None else nu_20c
        self.Re = self.v * self.D / self.nu
        self.L = L
        self.method = method
        self.C = C
        self.h = self.calc_head_loss()
        self.hf = self.h * self.L
        self.h = round(self.h, 4)
        self.hf = round(self.hf, 4)


    def calc_head_loss(self):
        match self.method:
            case 'Darcy-Weisbach':
                def calc_friction(self):
                   return fluids.friction_factor(self.Re, self.eD)
                if(self.Re < 2000):
                    self.flow_type = 'Laminar flow'
                    self.fr = 64 / self.Re
                elif (self.Re < 4000):
                    self.flow_type = 'Transitional flow'
                    self.fr = calc_friction(self)
                elif (self.Re >= 4000):
                    self.flow_type = 'Turbulent flow'
                    self.fr = calc_friction(self)
                h = self.fr * self.v**2 / (2 * self.D * G)
                self.fr = round(self.fr, 4)
                return h
            case 'Hazen-Williams':
                h = 10.674 * self.Q**1.852 / (self.D**4.87 * self.C**1.852)
                return h

# pipe1 = Pipe(Q=1, D=0.9, e=0.005, L=100)
# print(formater_str(pipe1.__dict__, ['Q', 'D', 'a', 'e', 'eD', 'v', 'nu', 'Re', 'L', 'method', 'flow_type', 'fr', 'h', 'hf']))
# pipe1 = Pipe(Q=1, D=0.9, L=100, method='Hazen-Williams', C=140)
# print(formater_str(pipe1.__dict__, ['Q', 'D', 'a', 'v', 'nu', 'Re', 'L', 'method', 'C', 'flow_type', 'fr', 'h', 'hf']))

# Perdidas de carga h 

"""
Q-> Caudal
D-> Diametro interno
e -> coef rugosidad absoluta del material
eD -> coef rugosidad relativa del material
Darcy (f, L?, D, Q, g)
Manning (n, D, Q, L)
Hazen-Williams (Q, C, D, L)

f -> v, D, rho, mu(viscosidad dinamica), e (Darcy) Re (rho (densidad), v, D, mu (viscocidad cinematica 0.1))
C -> D, f
eD -> e/D

"""

# print(fluids.friction_factor(Re=52222, eD=0.0001/0.5))