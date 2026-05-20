class Limites:
    def __init__(self, rut):
        # Asumimos que el rut trae al menos 8 numeros
        self.d3 = rut[2]
        self.d8 = rut[7]
        
        self.a = self.d3
        self.residuo = self.d8 % 3
        
        # Vemos que tipo de discontinuidad toca
        if self.residuo == 0:
            self.tipo = "Removible"
        elif self.residuo == 1:
            self.tipo = "De Salto"
        elif self.residuo == 2:
            self.tipo = "Infinita"

    def evaluar(self, x):
        # Caso 0: Removible
        if self.residuo == 0:
            if x == self.a:
                return 0
            else:
                return ((x ** 2) - (self.a ** 2)) / (x - self.a)
                
        # Caso 1: Salto
        elif self.residuo == 1:
            if x < self.a:
                return 2 * x
            else:
                return (3 * x) + 5
                
        # Caso 2: Infinita
        elif self.residuo == 2:
            if x == self.a:
                return None # aca hay asintota
            else:
                try:
                    return 1 / (x - self.a)
                except:
                    return None # por si acaso da error de division por cero

    def calcular_limites(self):
        fa = self.evaluar(self.a)
        
        if self.residuo == 0:
            izq = self.a + self.a
            der = self.a + self.a
            
        elif self.residuo == 1:
            izq = 2 * self.a
            der = (3 * self.a) + 5
            
        elif self.residuo == 2:
            izq = "-∞"
            der = "+∞"

        # Comprobamos si existe el limite y si es continua
        existe = (izq == der) and (izq != "-∞" and izq != "+∞")
        continua = existe and (izq == fa)

        return {
            "a": self.a,
            "izq": izq,
            "der": der,
            "fa": fa,
            "continua": continua,
            "tipo": self.tipo
        }

    def tabla_valores(self):
        # valores para acercarse por los lados
        deltas = [0.1, 0.01, 0.001]
        tabla_izq = []
        tabla_der = []
        
        for d in deltas:
            x_izq = self.a - d
            x_der = self.a + d
            
            # guardamos el x y el y redondeado a 4 decimales
            tabla_izq.append((round(x_izq, 4), round(self.evaluar(x_izq), 4)))
            tabla_der.append((round(x_der, 4), round(self.evaluar(x_der), 4)))
            
        return {"izq": tabla_izq, "der": tabla_der}

    def sacar_coordenadas(self):
        puntos = []
        paso = 20 / 200 # margen de 10 para cada lado, 200 puntos
        x_actual = self.a - 10
        
        for i in range(201):
            x = x_actual + (i * paso)
            
            if self.residuo == 2 and x == self.a:
                puntos.append((self.a, None))
                continue
                
            y = self.evaluar(x)
            
            # para que el grafico no se vuelva loco con el infinito
            if y is not None and (y > 1000 or y < -1000):
                y = None 
                
            puntos.append((x, y))
            
        return puntos
