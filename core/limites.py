class Limites:
    def __init__(self, digitos):
        # Guardamos los números del RUT que nos pide la pauta
        self.d1 = digitos[0]
        self.d2 = digitos[1]
        self.d3 = digitos[2]
        self.d4 = digitos[3]
        self.d5 = digitos[4]
        self.d8 = digitos[7]
        
        # El punto crítico (donde se rompe la gráfica) siempre es d3
        self.a = self.d3
        
        # Calculamos el residuo dividiendo en 3 para saber el tipo de discontinuidad
        self.residuo = self.d8 % 3
        
        if self.residuo == 0:
            self.tipo = "Removible"
        elif self.residuo == 1:
            self.tipo = "De Salto"
        else:
            self.tipo = "Infinita"

    def evaluar(self, x):
        # Esta función es como una calculadora manual. Le pasas un x y te da la y.
        
        if self.residuo == 0: # Caso Removible (Indeterminación 0/0)
            if x == self.a:
                return None # Da error matemático porque dividimos por cero
            return ((x - self.a) * (x + self.d1)) / (x - self.a)
                
        elif self.residuo == 1: # Caso de Salto (Función partida en dos)
            if x < self.a:
                return x + self.d2 # Venimos por la rama izquierda
            else:
                return x + self.d4 # Venimos por la rama derecha
                
        else: # Caso Infinito (Asíntota vertical)
            if x == self.a:
                return None # Es un muro infinito, no se puede evaluar
            return (self.d5 + 1) / (x - self.a)

    def calcular_limites(self):
        # Calculamos los límites laterales como si lo hiciéramos en el cuaderno
        if self.residuo == 0:
            # Simplificamos el (x-a) de arriba y abajo, nos queda solo (x+d1)
            izq = self.a + self.d1
            der = self.a + self.d1
            
        elif self.residuo == 1:
            # Evaluamos en cada tramo por separado
            izq = self.a + self.d2
            der = self.a + self.d4
            
        else:
            # Sabemos que el número de arriba es positivo, y el de abajo tiende a cero
            izq = "-∞" # Por la izquierda el cero es negativo, da menos infinito
            der = "+∞" # Por la derecha el cero es positivo, da más infinito

        # Vemos si la función se puede evaluar justo en 'a'
        fa = self.evaluar(self.a)
        
        return {"izq": izq, "der": der, "fa": fa}

    def tabla_valores(self):
        # Nos acercamos poquito a poco al punto crítico por ambos lados
        deltas = [0.1, 0.01, 0.001]
        tabla_izq = []
        tabla_der = []
        
        for d in deltas:
            x_izq = self.a - d
            x_der = self.a + d
            
            y_izq = self.evaluar(x_izq)
            y_der = self.evaluar(x_der)
            
            # Guardamos los puntos redondeados a 4 decimales. Si da error, escribimos "Indef"
            if y_izq is None:
                tabla_izq.append((round(x_izq, 4), "Indef"))
            else:
                tabla_izq.append((round(x_izq, 4), round(y_izq, 4)))
                
            if y_der is None:
                tabla_der.append((round(x_der, 4), "Indef"))
            else:
                tabla_der.append((round(x_der, 4), round(y_der, 4)))
                
        return {"izq": tabla_izq, "der": tabla_der}
    
    def punto_hueco(self):
        """
        Coordenada del 'hoyo' en la gráfica para la discontinuidad removible.
        Retorna (x, y) en x=a usando la función simplificada (x + d1),
        o None si no corresponde (salto o infinita).
        """
        if self.residuo == 0:
            return (self.a, self.a + self.d1)
        return None

    def sacar_coordenadas(self):
        # Creamos los puntitos para que el plotter dibuje la curva
        puntos = []
        paso = 0.1 # Avanzamos de a 0.1
        x_inicial = self.a - 10 # Empezamos 10 pasos atrás del punto crítico
        
        for i in range(200): # Hacemos 200 puntitos
            x = x_inicial + (i * paso)
            
            # Si es el caso infinito y estamos muy cerca de la asíntota, mejor saltarse ese punto
            # para que el gráfico no tire una línea fea recta de arriba a abajo
            if self.residuo == 2 and abs(x - self.a) < 0.05:
                puntos.append((x, None))
                continue
                
            y = self.evaluar(x)
            
            # Filtro: Si la Y se dispara a números gigantes, la cortamos
            if y is not None and (y > 1000 or y < -1000):
                y = None 
                
            puntos.append((x, y))
            
        return puntos

    # ==========================================================
    # MÉTODOS DE TEXTO EXPLICATIVO (LOS QUE CONECTAN CON LA UI)
    # ==========================================================

    def explicar_regla_seleccion(self):
        texto = f"Revisamos el dígito d8 del RUT, que es el {self.d8}.\n"
        texto += f"Calculamos {self.d8} dividido en 3 y el residuo nos da {self.residuo}.\n\n"
        
        if self.residuo == 0:
            texto += "Según la pauta, el residuo 0 significa que toca la Discontinuidad REMOVIBLE."
        elif self.residuo == 1:
            texto += "Según la pauta, el residuo 1 significa que toca la Discontinuidad DE SALTO."
        else:
            texto += "Según la pauta, el residuo 2 significa que toca la Discontinuidad INFINITA."
            
        return texto

    def paso_a_paso_limites(self):
        texto = f"=== CÁLCULO DE LÍMITES EN EL PUNTO a = {self.a} ===\n\n"
        
        if self.residuo == 0:
            texto += f"Paso 1: Tenemos la función f(x) = ((x - {self.a})(x + {self.d1})) / (x - {self.a})\n"
            texto += f"Paso 2: Si evaluamos directo en x = {self.a}, abajo nos da cero (Indeterminación 0/0).\n"
            texto += f"Paso 3: Tachamos el término común (x - {self.a}) arriba y abajo para simplificar.\n"
            texto += f"Paso 4: Nos queda la función limpia: f(x) = x + {self.d1}\n"
            texto += f"Paso 5: Calculamos los límites reemplazando la x:\n"
            texto += f"  - Límite por la izquierda: {self.a} + {self.d1} = {self.a + self.d1}\n"
            texto += f"  - Límite por la derecha: {self.a} + {self.d1} = {self.a + self.d1}"
            
        elif self.residuo == 1:
            texto += f"Paso 1: Tenemos una función partida en dos ramas en el punto x = {self.a}.\n"
            texto += f"Paso 2: Evaluamos el lado izquierdo usando la fórmula de esa rama (x + {self.d2}).\n"
            texto += f"  - Límite por la izquierda: {self.a} + {self.d2} = {self.a + self.d2}\n"
            texto += f"Paso 3: Evaluamos el lado derecho usando la fórmula de la otra rama (x + {self.d4}).\n"
            texto += f"  - Límite por la derecha: {self.a} + {self.d4} = {self.a + self.d4}"
            
        else:
            arriba = self.d5 + 1
            texto += f"Paso 1: La función es f(x) = {arriba} / (x - {self.a})\n"
            texto += f"Paso 2: El número de arriba siempre es la constante {arriba} (que es positiva).\n"
            texto += f"Paso 3: El número de abajo se hace cada vez más cercano a cero.\n"
            texto += f"Paso 4: Por la izquierda (x < {self.a}), lo de abajo da negativo. (Positivo / Negativo) = -∞\n"
            texto += f"Paso 5: Por la derecha (x > {self.a}), lo de abajo da positivo. (Positivo / Positivo) = +∞"
            
        return texto

    def justificar_discontinuidad(self):
        # Traemos los resultados de los límites calculados arriba
        res = self.calcular_limites()
        
        texto = "=== CONCLUSIÓN DE LA DISCONTINUIDAD ===\n\n"
        
        if self.residuo == 0:
            texto += f"Los dos límites laterales llegaron al mismo resultado ({res['izq']}), así que el límite SÍ EXISTE.\n"
            texto += f"Pero como la función original da error al evaluarla justo en x = {self.a}, queda un 'hoyo' en la gráfica.\n"
            texto += "Por esta razón, la discontinuidad se clasifica como REMOVIBLE."
            
        elif self.residuo == 1:
            texto += f"El límite de la izquierda nos dio {res['izq']} y el de la derecha nos dio {res['der']}.\n"
            texto += "Como dieron números distintos, matemáticamente el límite NO EXISTE.\n"
            texto += "La gráfica pega un brinco literal, por eso se clasifica como Discontinuidad DE SALTO."
            
        else:
            texto += "Los límites se disparan hacia el infinito (-∞ y +∞).\n"
            texto += "Como la gráfica no se junta nunca y forma un muro o asíntota vertical, el límite NO EXISTE.\n"
            texto += "Por tener este comportamiento, la discontinuidad se clasifica como INFINITA."
            
        return texto