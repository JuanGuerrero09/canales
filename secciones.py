from sympy.solvers import solve
from sympy import Symbol, sqrt, sin, acos, nsolve
# from utilidades import secante

class Canal(object):
    def __init__(self, n, So, Q):
        self.n = n
        self.So = So
        self.Q = Q
        self.y = None
        self.area = None
        self.perimetro_mojado = None
        self.radio_hidraulico = None
        self.ancho_superficial = None
        self.profundidad_hidraulica = None
        self.factor_de_seccion = None
        self.velocidad = None
        self.froude = None
        self.tipo_de_flujo = None

    def calc_propiedades(self):
        if self.Q is not None:
            if type(self.y) is not Symbol:
                self.velocidad = self.Q / self.area
                self.froude = self.velocidad / sqrt(9.81 * self.y)
                froude_value = str(self.froude)
                froude_value = float(froude_value)
                if froude_value > 1.0:
                    self.tipo_de_flujo = 'Supercrítico'
                elif froude_value == 1.0:
                    self.tipo_de_flujo = 'Crítico'
                else:
                    self.tipo_de_flujo = 'Subcrítico'

        else:
            pass

    def set_rugosidad(self, value):
        self.n = value

    def set_pendiente(self, value):
        self.So = value

    def set_caudal(self, value):
        self.Q = value

    def __str__(self) -> str:
        return f"Altura Normal: {self.y:.3f}\nRugosidad: {self.n}\nPendiente: {self.So}\nCaudal: {self.Q:.2f} m/s\nÁrea: {self.area:.3f}\nVelocidad: {self.velocidad:.3f}\nFroude: {self.froude:.3f}\nTipo de Flujo: {self.tipo_de_flujo}\n\n"
    
    # Áncho Superficial: {self.ancho_superficial:.3f}\n

class SeccionRectangular(Canal): 
    def __init__(self, n, So, Q, b, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.tipo_canal = 'Rectangular'
        self.b = b
        self.y = y


    def calc_propiedades(self):
        self.area = self.b * self.y
        self.perimetro_mojado = self.b + (self.y * 2)
        self.radio_hidraulico = self.area / self.perimetro_mojado
        self.ancho_superficial = self.b 
        self.profundidad_hidraulica = self.y
        self.factor_de_seccion = self.b * (self.y**1.5)
        super().calc_propiedades()


    def __str__(self):
        return f"\nCanal: {self.tipo_canal}\nDimensiones: \n\tBase: {self.b}\n\tAltura de agua: {self.y:.3f}\n{super().__str__()}"
    
    def caudal_manning(self):
        self.calc_propiedades()
        self.Q = (self.area * self.radio_hidraulico**(2/3) * self.So**0.5) / self.n
        self.calc_propiedades()
    
    def calc_yn(self):
        if(type(self.y) is Symbol):
            self.calc_propiedades()
            sol = (self.area * self.radio_hidraulico**(2/3) * self.So**0.5) / self.n
            self.y = nsolve(sol - self.Q, self.y, 1)
            self.calc_propiedades()
        else: 
            print('ya se tiene la altura: ' + str(self.y))
            self.calc_propiedades()
        return self.y 
    


class SeccionTrapezoidal(Canal):

    def __init__(self, n, So, Q, b, z, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.tipo_canal = 'Trapezoidal'
        self.b = b
        self.z = z
        self.y = y

    def calc_propiedades(self):
        print(self.y, self.z)
        self.area = (self.b + (self.y*self.z)) * self.y
        self.perimetro_mojado = self.b + (2 * self.y * (1 + self.z**2)**(1/2))
        self.radio_hidraulico = self.area / self.perimetro_mojado
        self.ancho_superficial = self.b  + (2 * self.y * self.z)
        self.profundidad_hidraulica = ((self.b + (self.z * self.y))* self.y) / (self.b + (2 * self.z * self.y))
        self.factor_de_seccion = ((self.b + (self.z * self.y))* self.y)**1.5 / (self.b + (2 * self.y * self.b))**0.5
        super().calc_propiedades()


  

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
            print('ya se tiene la altura: ' + str(self.y))
            self.calc_propiedades()
        return self.y
    
    def __str__(self):
        return f"Canal: {self.tipo_canal}\nDimensiones: \n\tBase: {self.b}\n\tPendiente: {self.z}\n\tAltura de agua: {self.y:.3f}\n{super().__str__()}"



class SeccionTriangular(Canal):
    def __init__(self, n, So, Q, z, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.tipo_canal = 'Triangular'
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

    def __str__(self):
        return f"Canal: {self.tipo_canal}\nDimensiones: \n\tPendiente: {self.z}\n\tAltura de agua: {self.y:.3f}\n{super().__str__()}"

    
class SeccionCircular(Canal): 
    def __init__(self, n, So, Q, D, y = Symbol('y')):
        super().__init__(n, So, Q)
        self.tipo_canal = 'Circular'
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
        return f"\nCanal: {self.tipo_canal}\nDimensiones: \n\tDiametro: {self.D}\n\tAltura de agua: {self.y:.3f}\n{super().__str__()}"
    
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
