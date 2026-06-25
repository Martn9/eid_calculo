class Conica:
    def __init__(self, digitos, dv):
        self.digitos = digitos
        self.dv_str = str(dv).upper()

        # Variables de la ecuacion general: Ax^2 + By^2 + Cx + Dy + E = 0
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0

        self.tipo = ""
        self.v = self._determinar_v()

        # Aqui voy guardando que reglas se aplicaron para poder explicarlas despues
        self.reglas_aplicadas = []

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

        # Calculo base segun la rubrica
        self.A = (d1 + d2) / self.v
        self.B = (d3 + d4) / self.v
        self.C = -(d5 + d6)
        self.D = -(d7 + d8)
        self.E = d1 + d3 + d5 + d7

        # Ajustes condicionales para forzar distintas conicas
        if d8 % 2 != 0:  # Si d8 es impar
            self.B = -self.B
            self.reglas_aplicadas.append("d8_impar")

        if d1 == d2:     # Si d1 y d2 son iguales
            self.B = self.A
            self.reglas_aplicadas.append("d1_igual_d2")

        if (d5 + d6) % 3 == 0:  # Multiplo de 3
            if d7 % 2 == 0:
                self.B = 0
                self.reglas_aplicadas.append("suma_d5d6_mult3_y_d7_par")
            else:
                self.A = 0
                self.reglas_aplicadas.append("suma_d5d6_mult3_y_d7_impar")

    def _clasificar(self):
        # Determinacion de la conica segun los coeficientes cuadraticos
        if self.A == 0 or self.B == 0:
            self.tipo = "Parábola"
        elif self.A == self.B:
            self.tipo = "Circunferencia"
        elif (self.A * self.B) > 0:
            self.tipo = "Elipse"
        elif (self.A * self.B) < 0:
            self.tipo = "Hipérbola"

    # ------------------------------------------------------------------
    # Datos de la forma canonica (centro y lado derecho)
    # Lo dejo en un metodo aparte porque lo usan tanto el desarrollo
    # inverso como la generacion de coordenadas.
    # ------------------------------------------------------------------
    def _datos_canonica(self):
        # Solo tiene sentido cuando hay x^2 e y^2 (no parabola)
        factor_x = self.C / self.A if self.A != 0 else 0
        factor_y = self.D / self.B if self.B != 0 else 0

        centro_x = -factor_x / 2
        centro_y = -factor_y / 2

        comp_x = (factor_x / 2) ** 2
        comp_y = (factor_y / 2) ** 2

        lado_derecho = -self.E + (self.A * comp_x) + (self.B * comp_y)

        return centro_x, centro_y, lado_derecho

    def paso_a_paso_canonico(self):
        pasos = []
        pasos.append("=== DESARROLLO HACIA LA FORMA CANÓNICA ===")
        pasos.append(f"Ecuación General: {self.A:.2f}x^2 + {self.B:.2f}y^2 + {self.C:.2f}x + {self.D:.2f}y + {self.E:.2f} = 0\n")

        # Logica para Circunferencia, Elipse e Hiperbola (Ambas variables al cuadrado)
        if self.tipo in ["Circunferencia", "Elipse", "Hipérbola"]:
            pasos.append("1. Agrupamos los términos con x y los términos con y, y pasamos el término independiente al otro lado:")
            pasos.append(f"({self.A:.2f}x^2 + {self.C:.2f}x) + ({self.B:.2f}y^2 + {self.D:.2f}y) = {-self.E:.2f}")

            pasos.append("\n2. Factorizamos los coeficientes principales (A y B) de los términos cuadráticos:")
            factor_x = self.C / self.A if self.A != 0 else 0
            factor_y = self.D / self.B if self.B != 0 else 0
            pasos.append(f"{self.A:.2f}(x^2 + {factor_x:.2f}x) + {self.B:.2f}(y^2 + {factor_y:.2f}y) = {-self.E:.2f}")

            pasos.append("\n3. Completamos el cuadrado sumando (b/2)^2 dentro del paréntesis y compensando en el lado derecho:")
            comp_x = (factor_x / 2) ** 2
            comp_y = (factor_y / 2) ** 2
            lado_derecho = -self.E + (self.A * comp_x) + (self.B * comp_y)

            pasos.append(f"{self.A:.2f}(x^2 + {factor_x:.2f}x + {comp_x:.2f}) + {self.B:.2f}(y^2 + {factor_y:.2f}y + {comp_y:.2f}) = {-self.E:.2f} + {self.A * comp_x:.2f} + {self.B * comp_y:.2f}")

            pasos.append("\n4. Expresamos como binomios al cuadrado:")
            pasos.append(f"{self.A:.2f}(x + {factor_x/2:.2f})^2 + {self.B:.2f}(y + {factor_y/2:.2f})^2 = {lado_derecho:.2f}")

            if self.tipo != "Circunferencia" and lado_derecho != 0:
                pasos.append("\n5. Dividimos toda la ecuación por el término de la derecha para igualar a 1:")
                denom_x = lado_derecho / self.A
                denom_y = lado_derecho / self.B
                pasos.append(f"(x + {factor_x/2:.2f})^2 / {denom_x:.2f} + (y + {factor_y/2:.2f})^2 / {denom_y:.2f} = 1")

            pasos.append(f"\nTipo identificado: {self.tipo}")

        # Logica para Parabola (Solo una variable al cuadrado)
        elif self.tipo == "Parábola":
            if self.A == 0:  # Parabola horizontal (y al cuadrado)
                pasos.append("1. Agrupamos los términos con 'y' y pasamos los términos con 'x' e independientes al otro lado:")
                pasos.append(f"{self.B:.2f}y^2 + {self.D:.2f}y = {-self.C:.2f}x + {-self.E:.2f}")

                pasos.append("\n2. Factorizamos el coeficiente principal de y:")
                factor_y = self.D / self.B
                pasos.append(f"{self.B:.2f}(y^2 + {factor_y:.2f}y) = {-self.C:.2f}x + {-self.E:.2f}")

                pasos.append("\n3. Completamos el cuadrado sumando (b/2)^2:")
                comp_y = (factor_y / 2) ** 2
                lado_derecho_E = -self.E + (self.B * comp_y)
                pasos.append(f"{self.B:.2f}(y + {factor_y/2:.2f})^2 = {-self.C:.2f}x + {lado_derecho_E:.2f}")

                if self.C != 0:
                    factor_x_derecho = lado_derecho_E / -self.C
                    pasos.append("\n4. Factorizamos el lado derecho para obtener el vértice:")
                    pasos.append(f"{self.B:.2f}(y + {factor_y/2:.2f})^2 = {-self.C:.2f}(x + {factor_x_derecho:.2f})")

            else:  # Parabola vertical (x al cuadrado)
                pasos.append("1. Agrupamos los términos con 'x' y pasamos los términos con 'y' e independientes al otro lado:")
                pasos.append(f"{self.A:.2f}x^2 + {self.C:.2f}x = {-self.D:.2f}y + {-self.E:.2f}")

                pasos.append("\n2. Factorizamos el coeficiente principal de x:")
                factor_x = self.C / self.A
                pasos.append(f"{self.A:.2f}(x^2 + {factor_x:.2f}x) = {-self.D:.2f}y + {-self.E:.2f}")

                pasos.append("\n3. Completamos el cuadrado sumando (b/2)^2:")
                comp_x = (factor_x / 2) ** 2
                lado_derecho_E = -self.E + (self.A * comp_x)
                pasos.append(f"{self.A:.2f}(x + {factor_x/2:.2f})^2 = {-self.D:.2f}y + {lado_derecho_E:.2f}")

                if self.D != 0:
                    factor_y_derecho = lado_derecho_E / -self.D
                    pasos.append("\n4. Factorizamos el lado derecho para obtener el vértice:")
                    pasos.append(f"{self.A:.2f}(x + {factor_x/2:.2f})^2 = {-self.D:.2f}(y + {factor_y_derecho:.2f})")

            pasos.append("\nTipo identificado: Parábola")

        return "\n".join(pasos)

    # ------------------------------------------------------------------
    # PROCEDIMIENTO INVERSO: desde la forma canonica de vuelta a la general
    # ------------------------------------------------------------------
    def paso_a_paso_inverso(self):
        pasos = []
        pasos.append("=== DESARROLLO INVERSO: DE LA FORMA CANÓNICA A LA GENERAL ===")
        pasos.append("Objetivo: partir del binomio al cuadrado y volver a Ax^2 + By^2 + Cx + Dy + E = 0\n")

        if self.tipo in ["Circunferencia", "Elipse", "Hipérbola"]:
            centro_x, centro_y, lado_derecho = self._datos_canonica()

            pasos.append("1. Partimos de la forma canónica con los binomios:")
            pasos.append(f"{self.A:.2f}(x - ({centro_x:.2f}))^2 + {self.B:.2f}(y - ({centro_y:.2f}))^2 = {lado_derecho:.2f}\n")

            pasos.append("2. Desarrollamos cada binomio al cuadrado (cuadrado de un binomio: (x - h)^2 = x^2 - 2hx + h^2):")
            pasos.append(f"(x - ({centro_x:.2f}))^2 = x^2 - {2*centro_x:.2f}x + {centro_x**2:.2f}")
            pasos.append(f"(y - ({centro_y:.2f}))^2 = y^2 - {2*centro_y:.2f}y + {centro_y**2:.2f}\n")

            pasos.append("3. Multiplicamos cada binomio desarrollado por su coeficiente A y B:")
            termino_cx = self.A * (-2 * centro_x)
            termino_indep_x = self.A * (centro_x ** 2)
            termino_dy = self.B * (-2 * centro_y)
            termino_indep_y = self.B * (centro_y ** 2)
            pasos.append(f"{self.A:.2f}*x^2 + ({termino_cx:.2f})x + ({termino_indep_x:.2f})")
            pasos.append(f"{self.B:.2f}*y^2 + ({termino_dy:.2f})y + ({termino_indep_y:.2f})\n")

            pasos.append("4. Juntamos todo en un solo lado y restamos el lado derecho:")
            constante_total = termino_indep_x + termino_indep_y - lado_derecho
            pasos.append(f"{self.A:.2f}x^2 + {self.B:.2f}y^2 + ({termino_cx:.2f})x + ({termino_dy:.2f})y + ({constante_total:.2f}) = 0\n")

            pasos.append("5. Comparamos con los coeficientes originales para verificar:")
            pasos.append(f"C debería ser {self.C:.2f}  ->  obtenido: {termino_cx:.2f}")
            pasos.append(f"D debería ser {self.D:.2f}  ->  obtenido: {termino_dy:.2f}")
            pasos.append(f"E debería ser {self.E:.2f}  ->  obtenido: {constante_total:.2f}")

        elif self.tipo == "Parábola":
            if self.A == 0:  # Parabola horizontal (y al cuadrado)
                factor_y = self.D / self.B
                centro_y = -factor_y / 2

                pasos.append("1. Partimos de la forma canónica (vértice) de la parábola horizontal:")
                pasos.append(f"{self.B:.2f}(y - ({centro_y:.2f}))^2 = {-self.C:.2f}x + (...)\n")

                pasos.append("2. Desarrollamos el binomio (y - k)^2 = y^2 - 2ky + k^2:")
                pasos.append(f"(y - ({centro_y:.2f}))^2 = y^2 - {2*centro_y:.2f}y + {centro_y**2:.2f}\n")

                termino_dy = self.B * (-2 * centro_y)
                termino_indep_y = self.B * (centro_y ** 2)

                pasos.append("3. Multiplicamos por B y pasamos todo a un solo lado (incluyendo el término en x):")
                pasos.append(f"{self.B:.2f}y^2 + ({termino_dy:.2f})y + {self.C:.2f}x + (constante) = 0\n")

                pasos.append("4. Comparamos con los coeficientes originales:")
                pasos.append(f"B debería ser {self.B:.2f}  ->  obtenido: {self.B:.2f}")
                pasos.append(f"D debería ser {self.D:.2f}  ->  obtenido: {termino_dy:.2f}")
                pasos.append(f"C debería ser {self.C:.2f} (acompaña a x)")

            else:  # Parabola vertical (x al cuadrado)
                factor_x = self.C / self.A
                centro_x = -factor_x / 2

                pasos.append("1. Partimos de la forma canónica (vértice) de la parábola vertical:")
                pasos.append(f"{self.A:.2f}(x - ({centro_x:.2f}))^2 = {-self.D:.2f}y + (...)\n")

                pasos.append("2. Desarrollamos el binomio (x - h)^2 = x^2 - 2hx + h^2:")
                pasos.append(f"(x - ({centro_x:.2f}))^2 = x^2 - {2*centro_x:.2f}x + {centro_x**2:.2f}\n")

                termino_cx = self.A * (-2 * centro_x)
                termino_indep_x = self.A * (centro_x ** 2)

                pasos.append("3. Multiplicamos por A y pasamos todo a un solo lado (incluyendo el término en y):")
                pasos.append(f"{self.A:.2f}x^2 + ({termino_cx:.2f})x + {self.D:.2f}y + (constante) = 0\n")

                pasos.append("4. Comparamos con los coeficientes originales:")
                pasos.append(f"A debería ser {self.A:.2f}  ->  obtenido: {self.A:.2f}")
                pasos.append(f"C debería ser {self.C:.2f}  ->  obtenido: {termino_cx:.2f}")
                pasos.append(f"D debería ser {self.D:.2f} (acompaña a y)")

        return "\n".join(pasos)

    # ------------------------------------------------------------------
    # EXPLICACION de como se construyeron A, B, C, D, E con las reglas del RUT
    # ------------------------------------------------------------------
    def explicar_construccion_coeficientes(self):
        d1, d2, d3, d4, d5, d6, d7, d8 = self.digitos
        lineas = []

        lineas.append("=== CONSTRUCCIÓN DE LOS COEFICIENTES A PARTIR DEL RUT ===")
        lineas.append(f"Dígitos del cuerpo: d1={d1}, d2={d2}, d3={d3}, d4={d4}, d5={d5}, d6={d6}, d7={d7}, d8={d8}")
        lineas.append(f"Valor v (depende del dígito verificador '{self.dv_str}'): v = {self.v}\n")

        lineas.append("Fórmulas base de la rúbrica:")
        lineas.append(f"A = (d1 + d2) / v = ({d1} + {d2}) / {self.v} = {(d1+d2)/self.v:.2f}")
        lineas.append(f"B = (d3 + d4) / v = ({d3} + {d4}) / {self.v} = {(d3+d4)/self.v:.2f}")
        lineas.append(f"C = -(d5 + d6) = -({d5} + {d6}) = {-(d5+d6)}")
        lineas.append(f"D = -(d7 + d8) = -({d7} + {d8}) = {-(d7+d8)}")
        lineas.append(f"E = d1 + d3 + d5 + d7 = {d1} + {d3} + {d5} + {d7} = {d1+d3+d5+d7}\n")

        lineas.append("Ajustes condicionales (reglas que cambian la cónica):")

        # Regla del d8 impar
        if d8 % 2 != 0:
            lineas.append(f"- d8 = {d8} es IMPAR, por eso B cambia de signo (B = -B). Esto puede generar una hipérbola.")
        else:
            lineas.append(f"- d8 = {d8} es PAR, así que B mantiene su signo.")

        # Regla d1 igual d2
        if d1 == d2:
            lineas.append(f"- d1 y d2 son IGUALES ({d1} = {d2}), entonces forzamos B = A. Con esto se obtiene una circunferencia.")
        else:
            lineas.append(f"- d1 ({d1}) y d2 ({d2}) son distintos, así que B no se iguala a A por esta regla.")

        # Regla suma d5+d6 multiplo de 3
        if (d5 + d6) % 3 == 0:
            lineas.append(f"- (d5 + d6) = {d5+d6} es MÚLTIPLO DE 3.")
            if d7 % 2 == 0:
                lineas.append(f"  Además d7 = {d7} es PAR, entonces B = 0 (queda una parábola en x).")
            else:
                lineas.append(f"  Además d7 = {d7} es IMPAR, entonces A = 0 (queda una parábola en y).")
        else:
            lineas.append(f"- (d5 + d6) = {d5+d6} no es múltiplo de 3, no se anula ningún coeficiente cuadrático.")

        lineas.append("\nCoeficientes finales después de aplicar las reglas:")
        lineas.append(f"A = {self.A:.2f} | B = {self.B:.2f} | C = {self.C} | D = {self.D} | E = {self.E}")
        lineas.append(f"Cónica resultante: {self.tipo}")

        return "\n".join(lineas)

    # ------------------------------------------------------------------
    # GENERACION DE COORDENADAS (sin librerias externas)
    # Idea: en vez de usar seno/coseno, despejo la variable y voy
    # recorriendo valores para ir sacando los puntos (x, y).
    # ------------------------------------------------------------------
    def sacar_coordenadas(self):
        puntos = []
        muestras = 300  # cuantos puntos calculo (mientras mas, mas suave)

        # ---------- CONICAS CON x^2 e y^2 (circunferencia, elipse, hiperbola) ----------
        if self.tipo in ["Circunferencia", "Elipse", "Hipérbola"]:
            centro_x, centro_y, lado_derecho = self._datos_canonica()

            # Tamaño aproximado de la figura en cada eje
            tamano_x = (abs(lado_derecho / self.A)) ** 0.5 if self.A != 0 else 1
            tamano_y = (abs(lado_derecho / self.B)) ** 0.5 if self.B != 0 else 1

            # La elipse/circunferencia es cerrada -> recorro solo su ancho.
            # La hiperbola es abierta -> recorro un poco mas para que se vean las ramas.
            if self.tipo == "Hipérbola":
                rango = max(tamano_x, tamano_y) * 3
            else:
                rango = max(tamano_x, tamano_y)

            inicio = centro_x - rango
            fin = centro_x + rango
            paso = (fin - inicio) / muestras

            # Recorro de izquierda a derecha buscando "tramos" validos.
            # Por cada tramo guardo la rama de arriba y la de abajo, y las
            # uno (arriba normal + abajo al reves) para que el dibujo quede continuo.
            rama_arriba = []
            rama_abajo = []

            x = inicio
            while x <= fin:
                # Despejo y:  B(y - centro_y)^2 = lado_derecho - A(x - centro_x)^2
                valor = (lado_derecho - self.A * (x - centro_x) ** 2) / self.B

                if valor >= 0:
                    raiz = valor ** 0.5
                    y_arriba = centro_y + raiz
                    y_abajo = centro_y - raiz
                    rama_arriba.append((x, y_arriba))
                    rama_abajo.append((x, y_abajo))
                else:
                    # Si se corto el tramo, cierro lo que tenia y lo guardo
                    if rama_arriba:
                        for punto in rama_arriba:
                            puntos.append(punto)
                        for punto in reversed(rama_abajo):
                            puntos.append(punto)
                        rama_arriba = []
                        rama_abajo = []
                x += paso

            # Guardo el ultimo tramo que haya quedado abierto
            if rama_arriba:
                for punto in rama_arriba:
                    puntos.append(punto)
                for punto in reversed(rama_abajo):
                    puntos.append(punto)

        # ---------- PARABOLA ----------
        elif self.tipo == "Parábola":
            if self.B == 0:
                # Parabola vertical (x^2): recorro x y despejo y
                # A x^2 + C x + D y + E = 0  ->  y = -(A x^2 + C x + E) / D
                centro_x = -(self.C / self.A) / 2 if self.A != 0 else 0
                inicio = centro_x - 10
                fin = centro_x + 10
                paso = (fin - inicio) / muestras

                x = inicio
                while x <= fin:
                    if self.D != 0:
                        y = -(self.A * x ** 2 + self.C * x + self.E) / self.D
                        puntos.append((x, y))
                    x += paso

            else:
                # Parabola horizontal (y^2): recorro y y despejo x
                # B y^2 + D y + C x + E = 0  ->  x = -(B y^2 + D y + E) / C
                centro_y = -(self.D / self.B) / 2
                inicio = centro_y - 10
                fin = centro_y + 10
                paso = (fin - inicio) / muestras

                y = inicio
                while y <= fin:
                    if self.C != 0:
                        x = -(self.B * y ** 2 + self.D * y + self.E) / self.C
                        puntos.append((x, y))
                    y += paso

        return puntos
