class Conica:
    def __init__(self, digitos, dv):
        self.digitos = digitos
        self.dv = dv
        self.tipo = ""
        
        # Nuestras 5 letras de la ecuación general
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        
        # Ejecutamos el cálculo nada más al crear la cónica
        self.calcular_coeficientes()
        self.clasificar_figura()

    def calcular_coeficientes(self):
        # Desarmamos la lista de dígitos para que sea más fácil usarlos
        d1, d2, d3, d4, d5, d6, d7, d8 = self.digitos
        
        # Sacamos el valor de v según el dígito verificador
        if str(self.dv).upper() == 'K':
            v = 10
        elif str(self.dv) == '0':
            v = 11
        else:
            v = int(self.dv)
            
        # Aplicamos las fórmulas que salen en la pauta
        self.A = (d1 + d2) / v
        self.B = (d3 + d4) / v
        self.C = -(d5 + d6)
        self.D = -(d7 + d8)
        self.E = d1 + d3 + d5 + d7

        # Reglas extra del profesor para alterar la figura
        if d8 % 2 != 0:       # Si d8 es impar, B cambia de signo
            self.B = -self.B
            
        if d1 == d2:          # Si d1 y d2 son iguales, forzamos circunferencia
            self.B = self.A
            
        if (d5 + d6) % 3 == 0:  # Si es múltiplo de 3, matamos A o B para que sea parábola
            if d7 % 2 == 0:
                self.B = 0
            else:
                self.A = 0

    def clasificar_figura(self):
        # Para saber qué figura es, solo miramos los números que acompañan al cuadrado (A y B)
        if self.A == 0 or self.B == 0:
            self.tipo = "Parábola"
        elif self.A == self.B:
            self.tipo = "Circunferencia"
        elif (self.A * self.B) > 0:
            self.tipo = "Elipse"
        else:
            self.tipo = "Hipérbola"

    def paso_a_paso_canonico(self):
        # Armamos el texto sumando strings (como se hace normalmente)
        texto = "=== DE ECUACIÓN GENERAL A FORMA CANÓNICA ===\n\n"
        texto += f"Ecuación inicial: {self.A:.2f}x² + {self.B:.2f}y² + {self.C:.2f}x + {self.D:.2f}y + {self.E:.2f} = 0\n\n"
        
        if self.tipo in ["Circunferencia", "Elipse", "Hipérbola"]:
            texto += "Paso 1: Juntamos las 'x' a un lado, las 'y' al otro, y pasamos el número solo a la derecha.\n"
            texto += "Paso 2: Le sacamos el factor común a los números que acompañan al x² y al y².\n"
            texto += "Paso 3: Hacemos la 'completación de cuadrados' (sumamos la mitad del número del medio al cuadrado).\n"
            texto += "Paso 4: Lo que agregamos a la izquierda, también lo sumamos a la derecha para equilibrar.\n"
            texto += "Paso 5: Comprimimos la ecuación dejándola como binomios al cuadrado perfectos.\n"
            if self.tipo != "Circunferencia":
                texto += "Paso 6: Como es Elipse o Hipérbola, dividimos todo por el número de la derecha para igualar a 1.\n"
        else:
            texto += "Paso 1: Dejamos la letra que está al cuadrado a la izquierda y pasamos todo lo demás a la derecha.\n"
            texto += "Paso 2: Factorizamos el número principal.\n"
            texto += "Paso 3: Hacemos la completación de cuadrados sumando la mitad del término lineal al cuadrado.\n"
            texto += "Paso 4: Comprimimos la izquierda como un binomio al cuadrado perfecto.\n"
            texto += "Paso 5: Factorizamos la derecha para que el vértice (h, k) quede a la vista.\n"
            
        texto += f"\n>> El análisis matemático indica que la figura es una {self.tipo}."
        return texto

    def paso_a_paso_inverso(self):
        texto = "=== PROCEDIMIENTO INVERSO ===\n\n"
        texto += "Para retroceder y volver a la ecuación original hacemos esto:\n"
        texto += "1. Agarramos la ecuación canónica y miramos los binomios al cuadrado (x-h)² y (y-k)².\n"
        texto += "2. Los resolvemos usando la vieja regla: El primero al cuadrado, más el doble del primero por el segundo, más el segundo al cuadrado.\n"
        texto += "3. Multiplicamos eso por los números que estaban afuera del paréntesis.\n"
        texto += "4. Si nos quedó alguna fracción abajo, multiplicamos toda la ecuación por el Mínimo Común Múltiplo para matarla.\n"
        texto += "5. Pasamos todo para el lado izquierdo para que quede igualado a 0.\n"
        texto += "6. Sumamos los números sueltos y recuperamos la ecuación general.\n"
        return texto

    def sacar_coordenadas(self):
        puntos = []
        
        # Sacamos un centro de referencia usando una fórmula básica para no buscar puntos al infinito
        centro_x = -self.C / (2 * self.A) if self.A != 0 else 0
        centro_y = -self.D / (2 * self.B) if self.B != 0 else 0
        
        # Si es Parábola Horizontal (no tiene X al cuadrado)
        if self.A == 0:
            # Hacemos un loop simple alrededor del centro
            for i in range(-1000, 1000):
                y = centro_y + (i * 0.1)
                # Despejamos X a la mala
                x = (-self.B*(y**2) - self.D*y - self.E) / self.C
                puntos.append((x, y))
                
        # Si es Parábola Vertical (no tiene Y al cuadrado)
        elif self.B == 0:
            for i in range(-1000, 1000):
                x = centro_x + (i * 0.1)
                # Despejamos Y
                y = (-self.A*(x**2) - self.C*x - self.E) / self.D
                puntos.append((x, y))
                
        # Si es Elipse, Hipérbola o Circunferencia (Ambas al cuadrado)
        else:
            # Usamos la fórmula general cuadrática para despejar 'Y'
            a = self.B
            b = self.D
            
            for i in range(-3000, 3000):
                x = centro_x + (i * 0.1)
                # Todo lo que no tiene 'y' lo tratamos como la constante 'c'
                c = self.A*(x**2) + self.C*x + self.E
                
                # Lo que va adentro de la raíz
                discriminante = (b**2) - (4*a*c)
                
                # Si es positivo, se puede sacar raíz cuadrada
                if discriminante >= 0:
                    raiz = discriminante ** 0.5
                    
                    y1 = (-b + raiz) / (2*a)
                    y2 = (-b - raiz) / (2*a)
                    
                    puntos.append((x, y1))
                    puntos.append((x, y2))
                    
        return puntos
