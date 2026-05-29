class Conica:
    def __init__(self, digitos, dv):
        self.digitos = digitos
        self.dv_str = str(dv).upper()
        
        # Variables de la ecuación general: Ax^2 + By^2 + Cx + Dy + E = 0
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        
        self.tipo = ""
        self.v = self._determinar_v()
        
        self._calcular_coeficientes()
        self._clasificar()

    def _determinar_v(self):
        if self.dv_str == 'K':
            return 10
        elif self.dv_str == '0':
            return 11
        else:
            return int(self.dv_str)

    def _calcular_coeficientes(self):
        d1, d2, d3, d4, d5, d6, d7, d8 = self.digitos
        
        # Cálculo base según la rúbrica
        self.A = (d1 + d2) / self.v
        self.B = (d3 + d4) / self.v
        self.C = -(d5 + d6)
        self.D = -(d7 + d8)
        self.E = d1 + d3 + d5 + d7

        # Ajustes condicionales para forzar distintas cónicas
        if d8 % 2 != 0:  # Si d8 es impar
            self.B = -self.B
            
        if d1 == d2:     # Si d1 y d2 son iguales
            self.B = self.A
            
        if (d5 + d6) % 3 == 0:  # Múltiplo de 3
            if d7 % 2 == 0:
                self.B = 0
            else:
                self.A = 0

    def _clasificar(self):
        # Determinación de la cónica según los coeficientes cuadráticos
        if self.A == 0 or self.B == 0:
            self.tipo = "Parábola"
        elif self.A == self.B:
            self.tipo = "Circunferencia"
        elif (self.A * self.B) > 0:
            self.tipo = "Elipse"
        elif (self.A * self.B) < 0:
            self.tipo = "Hipérbola"

    def paso_a_paso_canonico(self):
        pasos = []
        pasos.append("=== DESARROLLO HACIA LA FORMA CANÓNICA ===")
        pasos.append(f"Ecuación General: {self.A:.2f}x^2 + {self.B:.2f}y^2 + {self.C:.2f}x + {self.D:.2f}y + {self.E:.2f} = 0\n")

        # Lógica para Circunferencia, Elipse e Hipérbola (Ambas variables al cuadrado)
        if self.tipo in ["Circunferencia", "Elipse", "Hipérbola"]:
            pasos.append("1. Agrupamos los términos con x y los términos con y, y pasamos el término independiente al otro lado:")
            pasos.append(f"({self.A:.2f}x^2 + {self.C:.2f}x) + ({self.B:.2f}y^2 + {self.D:.2f}y) = {-self.E:.2f}")

            pasos.append("\n2. Factorizamos los coeficientes principales (A y B) de los términos cuadráticos:")
            fact_x = self.C / self.A if self.A != 0 else 0
            fact_y = self.D / self.B if self.B != 0 else 0
            pasos.append(f"{self.A:.2f}(x^2 + {fact_x:.2f}x) + {self.B:.2f}(y^2 + {fact_y:.2f}y) = {-self.E:.2f}")

            pasos.append("\n3. Completamos el cuadrado sumando (b/2)^2 dentro del paréntesis y compensando en el lado derecho:")
            comp_x = (fact_x / 2) ** 2
            comp_y = (fact_y / 2) ** 2
            lado_derecho = -self.E + (self.A * comp_x) + (self.B * comp_y)
            
            pasos.append(f"{self.A:.2f}(x^2 + {fact_x:.2f}x + {comp_x:.2f}) + {self.B:.2f}(y^2 + {fact_y:.2f}y + {comp_y:.2f}) = {-self.E:.2f} + {self.A * comp_x:.2f} + {self.B * comp_y:.2f}")
            
            pasos.append("\n4. Expresamos como binomios al cuadrado:")
            pasos.append(f"{self.A:.2f}(x + {fact_x/2:.2f})^2 + {self.B:.2f}(y + {fact_y/2:.2f})^2 = {lado_derecho:.2f}")

            if self.tipo != "Circunferencia" and lado_derecho != 0:
                pasos.append("\n5. Dividimos toda la ecuación por el término de la derecha para igualar a 1:")
                denom_x = lado_derecho / self.A
                denom_y = lado_derecho / self.B
                pasos.append(f"(x + {fact_x/2:.2f})^2 / {denom_x:.2f} + (y + {fact_y/2:.2f})^2 / {denom_y:.2f} = 1")
            
            pasos.append(f"\nTipo identificado: {self.tipo}")

        # Lógica para Parábola (Solo una variable al cuadrado)
        elif self.tipo == "Parábola":
            if self.A == 0: # Parábola horizontal (y al cuadrado)
                pasos.append("1. Agrupamos los términos con 'y' y pasamos los términos con 'x' e independientes al otro lado:")
                pasos.append(f"{self.B:.2f}y^2 + {self.D:.2f}y = {-self.C:.2f}x + {-self.E:.2f}")
                
                pasos.append("\n2. Factorizamos el coeficiente principal de y:")
                fact_y = self.D / self.B
                pasos.append(f"{self.B:.2f}(y^2 + {fact_y:.2f}y) = {-self.C:.2f}x + {-self.E:.2f}")
                
                pasos.append("\n3. Completamos el cuadrado sumando (b/2)^2:")
                comp_y = (fact_y / 2) ** 2
                lado_derecho_E = -self.E + (self.B * comp_y)
                pasos.append(f"{self.B:.2f}(y + {fact_y/2:.2f})^2 = {-self.C:.2f}x + {lado_derecho_E:.2f}")
                
                if self.C != 0:
                    fact_x_derecho = lado_derecho_E / -self.C
                    pasos.append("\n4. Factorizamos el lado derecho para obtener el vértice:")
                    pasos.append(f"{self.B:.2f}(y + {fact_y/2:.2f})^2 = {-self.C:.2f}(x + {fact_x_derecho:.2f})")
                    
            else: # Parábola vertical (x al cuadrado)
                pasos.append("1. Agrupamos los términos con 'x' y pasamos los términos con 'y' e independientes al otro lado:")
                pasos.append(f"{self.A:.2f}x^2 + {self.C:.2f}x = {-self.D:.2f}y + {-self.E:.2f}")
                
                pasos.append("\n2. Factorizamos el coeficiente principal de x:")
                fact_x = self.C / self.A
                pasos.append(f"{self.A:.2f}(x^2 + {fact_x:.2f}x) = {-self.D:.2f}y + {-self.E:.2f}")
                
                pasos.append("\n3. Completamos el cuadrado sumando (b/2)^2:")
                comp_x = (fact_x / 2) ** 2
                lado_derecho_E = -self.E + (self.A * comp_x)
                pasos.append(f"{self.A:.2f}(x + {fact_x/2:.2f})^2 = {-self.D:.2f}y + {lado_derecho_E:.2f}")
                
                if self.D != 0:
                    fact_y_derecho = lado_derecho_E / -self.D
                    pasos.append("\n4. Factorizamos el lado derecho para obtener el vértice:")
                    pasos.append(f"{self.A:.2f}(x + {fact_x/2:.2f})^2 = {-self.D:.2f}(y + {fact_y_derecho:.2f})")
            
            pasos.append("\nTipo identificado: Parábola")

        return "\n".join(pasos)

    def sacar_coordenadas(self):
        # Esta función dependerá de los límites del plano cartesiano que definas en plotter.py.
        # Por ahora retorna un arreglo vacío listo para que lo conecten con el renderizador.
        puntos = []
        return puntos