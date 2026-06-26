class Limites:
    def __init__(self, digitos):
        # DEFENSA: Se extraen los dígitos individuales del RUT del líder según la pauta
        self.d1 = digitos[0]
        self.d2 = digitos[1]
        self.d3 = digitos[2]
        self.d4 = digitos[3]
        self.d5 = digitos[4]
        self.d8 = digitos[7]
        
        # DEFENSA: El punto crítico 'a' por pauta siempre se define como el dígito d3
        self.a = self.d3
        self.residuo = self.d8 % 3
        
        # Clasificamos el tipo de discontinuidad según el residuo de d8 % 3
        if self.residuo == 0:
            self.tipo = "Removible"
        elif self.residuo == 1:
            self.tipo = "De Salto"
        elif self.residuo == 2:
            self.tipo = "Infinita"

    def evaluar(self, x):
        """ DEFENSA: Evalúa un punto x cualquiera en la función por tramos generada """
        # Caso 0: Removible -> f(x) = ((x-a)(x+d1)) / (x-a)
        if self.residuo == 0:
            if x == self.a:
                return None # Indefinición matemática en el punto crítico (0/0)
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
                return None # Asíntota vertical en x=a
            else:
                try:
                    return (self.d5 + 1) / (x - self.a)
                except ZeroDivisionError:
                    return None

    def calcular_limites(self):
        """ DEFENSA: Calcula los límites laterales analíticamente sin librerías """
        if self.residuo == 0:
            izq = self.a + self.d1
            der = self.a + self.d1
            
        elif self.residuo == 1:
            izq = self.a + self.d2
            der = self.a + self.d4
            
        elif self.residuo == 2:
            izq = "-∞"
            der = "+∞"

        fa = self.evaluar(self.a)
        
        # El límite existe si los laterales son iguales y finitos
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
        """ Genera los valores para la tabla de evidencia computacional """
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
        """ Genera el arreglo de puntos para el graficador plotter.py """
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

    # =========================================================================
    # NUEVOS MÉTODOS DE TEXTO EXIGIDOS POR EL EID.PDF (FASE 6)
    # =========================================================================

    def explicar_regla_seleccion(self):
        """ FASE 6: Explica la selección automática de la función basada en d8 """
        texto = f"Análisis del Dígito d8:\n"
        texto += f"- El octavo dígito de tu RUT es d8 = {self.d8}.\n"
        texto += f"- Evaluando la operación matemática d8 % 3 obtenemos un residuo de {self.residuo}.\n\n"
        
        if self.residuo == 0:
            texto += "Resultado de la Regla: Residuo igual a 0. El sistema genera de forma automática un escenario con Discontinuidad REMOVIBLE."
        elif self.residuo == 1:
            texto += "Resultado de la Regla: Residuo igual a 1. El sistema genera de forma automática un escenario con Discontinuidad DE SALTO."
        elif self.residuo == 2:
            texto += "Resultado de la Regla: Residuo igual a 2. El sistema genera de forma automática un escenario con Discontinuidad INFINITA."
            
        return texto

    def paso_a_paso_limites(self):
        """ FASE 6: Imprime el desarrollo algebraico paso a paso para calcular los límites """
        texto = f"=== DESARROLLO MATEMÁTICO: LÍMITES LATERALES EN x = {self.a} ===\n\n"
        
        if self.residuo == 0:
            texto += f"1. Planteamos la función original: f(x) = ((x - {self.a})(x + {self.d1})) / (x - {self.a})\n"
            texto += f"2. Al evaluar directamente en x = {self.a}, el denominador se anula dando una indeterminación de tipo 0/0.\n"
            texto += f"3. Para romper la indeterminación, simplificamos el factor común (x - {self.a}) tanto arriba como abajo.\n"
            texto += f"4. Obtenemos la expresión limpia: f(x) = x + {self.d1}\n"
            texto += f"5. Calculamos los límites laterales evaluando de forma directa en el punto crítico:\n"
            texto += f"   - Límite Izquierdo (x -> {self.a}-): {self.a} + {self.d1} = {self.a + self.d1}\n"
            texto += f"   - Límite Derecho   (x -> {self.a}+): {self.a} + {self.d1} = {self.a + self.d1}"
            
        elif self.residuo == 1:
            texto += f"1. Planteamos la función estructurada por tramos según el punto frontera {self.a}:\n"
            texto += f"   - Tramo Izquierdo (si x < {self.a}): f(x) = x + {self.d2}\n"
            texto += f"   - Tramo Derecho   (si x >= {self.a}): f(x) = x + {self.d4}\n"
            texto += f"2. Evaluamos el Límite Izquierdo (x -> {self.a}-) usando la primera regla de correspondencia:\n"
            texto += f"   Reemplazamos x = {self.a} en (x + {self.d2}) -> {self.a} + {self.d2} = {self.a + self.d2}\n"
            texto += f"3. Evaluamos el Límite Derecho (x -> {self.a}+) usando la segunda regla de correspondencia:\n"
            texto += f"   Reemplazamos x = {self.a} en (x + {self.d4}) -> {self.a} + {self.d4} = {self.a + self.d4}"
            
        elif self.residuo == 2:
            num = self.d5 + 1
            texto += f"1. Planteamos la función con asíntota: f(x) = {num} / (x - {self.a})\n"
            texto += f"2. El numerador corresponde a una constante real fija positiva ({num}).\n"
            texto += f"3. Al acercarnos al valor crítico x = {self.a}, el denominador tiende a 0, haciendo que la fracción crezca de manera desmedida.\n"
            texto += f"4. Realizamos un estudio riguroso de signos laterales:\n"
            texto += f"   - Por la Izquierda (x < {self.a}): El denominador toma valores negativos pequeños. Fracción (+ / -) -> Límite = -∞\n"
            texto += f"   - Por la Derecha   (x > {self.a}): El denominador toma valores positivos pequeños. Fracción (+ / +) -> Límite = +∞"
            
        return texto

    def justificar_discontinuidad(self):
        """ FASE 6: Genera la justificación conceptual de continuidad/discontinuidad """
        res = self.calcular_limites()
        
        texto = "=== JUSTIFICACIÓN MATEMÁTICA Y CONCLUSIÓN DE CONTINUIDAD ===\n\n"
        if self.residuo == 0:
            texto += f"Análisis: El límite izquierdo y derecho convergen al mismo valor numérico ({res['izq']}), por ende el límite EXISTE.\n"
            texto += f"Sin embargo, al evaluar f({self.a}) la función no está definida por la división por cero original.\n"
            texto += "Conclusión: Dado que el límite existe pero el punto no pertenece al dominio, la discontinuidad es REMOVIBLE."
        elif self.residuo == 1:
            texto += f"Análisis: El límite izquierdo es {res['izq']} y el límite derecho es {res['der']}.\n"
            texto += "Dado que ambos valores laterales no coinciden, se determina formalmente que el límite NO EXISTE.\n"
            texto += "Conclusión: Al no existir un punto de convergencia único, se genera una ruptura o Discontinuidad DE SALTO."
        elif self.residuo == 2:
            texto += f"Análisis: Al evaluar el comportamiento lateral, la función diverge y tiende hacia los valores -∞ y +∞.\n"
            texto += f"Esto demuestra geométricamente la existencia de una asíntota vertical en la recta x = {self.a}.\n"
            texto += "Conclusión: La presencia de un comportamiento asintótico define una Discontinuidad INFINITA."
            
        return texto