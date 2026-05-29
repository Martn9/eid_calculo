class Limites:
    def __init__(self, digitos):
        # La rúbrica exige extraer los dígitos para construir la función
        self.d1 = digitos[0]
        self.d2 = digitos[1]
        self.d3 = digitos[2]
        self.d4 = digitos[3]
        self.d5 = digitos[4]
        self.d8 = digitos[7]
        
        self.a = self.d3
        self.residuo = self.d8 % 3
        
        # Clasificamos el tipo de discontinuidad según el residuo
        if self.residuo == 0:
            self.tipo = "Removible"
        elif self.residuo == 1:
            self.tipo = "De Salto"
        elif self.residuo == 2:
            self.tipo = "Infinita"

    def evaluar(self, x):
        # Caso 0: Removible -> f1(x) = ((x-a)(x+d1)) / (x-a)
        if self.residuo == 0:
            if x == self.a:
                return None # Indefinición en x=a
            else:
                try:
                    return ((x - self.a) * (x + self.d1)) / (x - self.a)
                except ZeroDivisionError:
                    return None
                
        # Caso 1: Salto -> x+d2 si x < a, x+d4 si x >= a
        elif self.residuo == 1:
            if x < self.a:
                return x + self.d2
            else:
                return x + self.d4
                
        # Caso 2: Infinita -> (d5+1) / (x-a)
        elif self.residuo == 2:
            if x == self.a:
                return None # Asíntota
            else:
                try:
                    return (self.d5 + 1) / (x - self.a)
                except ZeroDivisionError:
                    return None

    def calcular_limites(self):
        # Cálculos manuales de los límites según la función generada
        if self.residuo == 0:
            izq = self.a + self.d1
            der = self.a + self.d1
            
        elif self.residuo == 1:
            izq = self.a + self.d2
            der = self.a + self.d4
            
        elif self.residuo == 2:
            # (d5+1) siempre es positivo. Si x se acerca por izq (x < a), (x-a) es negativo.
            izq = "-∞"
            der = "+∞"

        fa = self.evaluar(self.a)
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
        deltas = [0.1, 0.01, 0.001]
        tabla_izq = []
        tabla_der = []
        
        for d in deltas:
            x_izq = self.a - d
            x_der = self.a + d
            
            y_izq = self.evaluar(x_izq)
            y_der = self.evaluar(x_der)
            
            tabla_izq.append((round(x_izq, 4), round(y_izq, 4) if y_izq is not None else "Indef"))
            tabla_der.append((round(x_der, 4), round(y_der, 4) if y_der is not None else "Indef"))
            
        return {"izq": tabla_izq, "der": tabla_der}

    def sacar_coordenadas(self):
        puntos = []
        paso = 20 / 200 
        x_actual = self.a - 10
        
        for i in range(201):
            x = x_actual + (i * paso)
            
            if self.residuo == 2 and abs(x - self.a) < 0.05:
                puntos.append((x, None))
                continue
                
            y = self.evaluar(x)
            
            if y is not None and (y > 1000 or y < -1000):
                y = None 
                
            puntos.append((x, y))
            
        return puntos