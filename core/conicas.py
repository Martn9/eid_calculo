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

    def ecuacion_general_str(self):
        """Devuelve la ecuación general con los coeficientes reales del RUT."""
        return (f"{self.A:.2f}x² + {self.B:.2f}y² + "
                f"{self.C:.2f}x + {self.D:.2f}y + {self.E:.2f} = 0")

    def forma_canonica(self):
        """
        Calcula numéricamente la forma canónica completando cuadrados
        (sin librerías). Devuelve un diccionario con los valores reales:
        centro/vértice, constante de la derecha y semiejes cuando aplica.
        """
        datos = {"tipo": self.tipo}

        # --- PARÁBOLA DE EJE VERTICAL (B = 0): (x-h)² = (-D/A)(y - k) ---
        if self.B == 0:
            h = -self.C / (2 * self.A)
            k = (self.A * h ** 2 - self.E) / self.D
            p = -self.D / self.A            # (x-h)² = p (y - k)
            datos.update({"orientacion": "vertical", "h": h, "k": k, "p": p})

        # --- PARÁBOLA DE EJE HORIZONTAL (A = 0): (y-k)² = (-C/B)(x - h) ---
        elif self.A == 0:
            k = -self.D / (2 * self.B)
            h = (self.B * k ** 2 - self.E) / self.C
            p = -self.C / self.B            # (y-k)² = p (x - h)
            datos.update({"orientacion": "horizontal", "h": h, "k": k, "p": p})

        # --- CENTRALES: A(x-h)² + B(y-k)² = M ---
        else:
            h = -self.C / (2 * self.A)
            k = -self.D / (2 * self.B)
            M = self.A * h ** 2 + self.B * k ** 2 - self.E
            datos.update({"h": h, "k": k, "M": M})

            if self.tipo == "Circunferencia":
                datos["r2"] = M / self.A    # (x-h)² + (y-k)² = r²
            else:
                # Dividimos por M:  (x-h)²/(M/A) + (y-k)²/(M/B) = 1
                datos["den_x"] = M / self.A
                datos["den_y"] = M / self.B
        return datos

    def paso_a_paso_canonico(self):
        c = self.forma_canonica()
        texto = "=== DE ECUACIÓN GENERAL A FORMA CANÓNICA ===\n\n"
        texto += f"Ecuación general: {self.ecuacion_general_str()}\n\n"

        # ---------- CÍRCULO / ELIPSE / HIPÉRBOLA ----------
        if self.tipo in ["Circunferencia", "Elipse", "Hipérbola"]:
            h, k, M = c["h"], c["k"], c["M"]
            texto += f"Paso 1: Agrupamos términos en x y en y, y pasamos E al otro lado:\n"
            texto += f"   {self.A:.2f}x² + {self.C:.2f}x + {self.B:.2f}y² + {self.D:.2f}y = {-self.E:.2f}\n\n"
            texto += f"Paso 2: Factor común {self.A:.2f} en x y {self.B:.2f} en y:\n"
            texto += f"   {self.A:.2f}(x² + {self.C/self.A:.2f}x) + {self.B:.2f}(y² + {self.D/self.B:.2f}y) = {-self.E:.2f}\n\n"
            texto += f"Paso 3: Completamos cuadrados. Mitad al cuadrado:\n"
            texto += f"   x: ({self.C/self.A/2:.2f})² = {(self.C/self.A/2)**2:.2f}   |   y: ({self.D/self.B/2:.2f})² = {(self.D/self.B/2)**2:.2f}\n\n"
            texto += f"Paso 4: Sumamos lo mismo (x factor) a la derecha para equilibrar:\n"
            texto += f"   {self.A:.2f}(x {'-' if h>=0 else '+'} {abs(h):.2f})² + {self.B:.2f}(y {'-' if k>=0 else '+'} {abs(k):.2f})² = {M:.2f}\n\n"

            if self.tipo == "Circunferencia":
                r2 = c["r2"]
                r = r2 ** 0.5 if r2 > 0 else 0
                texto += f"Paso 5: Dividimos por {self.A:.2f}. FORMA CANÓNICA:\n"
                texto += f"   (x {'-' if h>=0 else '+'} {abs(h):.2f})² + (y {'-' if k>=0 else '+'} {abs(k):.2f})² = {r2:.2f}\n"
                texto += f"   Centro = ({h:.2f}, {k:.2f})   Radio = {r:.2f}\n"
            else:
                dx, dy = c["den_x"], c["den_y"]
                texto += f"Paso 5: Dividimos todo por {M:.2f} para igualar a 1. FORMA CANÓNICA:\n"
                texto += f"   (x {'-' if h>=0 else '+'} {abs(h):.2f})²/({dx:.2f}) + (y {'-' if k>=0 else '+'} {abs(k):.2f})²/({dy:.2f}) = 1\n"
                texto += f"   Centro = ({h:.2f}, {k:.2f})\n"

        # ---------- PARÁBOLA ----------
        else:
            h, k, p = c["h"], c["k"], c["p"]
            if c["orientacion"] == "vertical":
                texto += f"Paso 1: Como B = 0, dejamos x² a la izquierda:\n"
                texto += f"   {self.A:.2f}x² + {self.C:.2f}x = {-self.D:.2f}y {'-' if self.E>=0 else '+'} {abs(self.E):.2f}\n\n"
                texto += f"Paso 2: Factor común {self.A:.2f} y completamos cuadrado en x:\n"
                texto += f"   mitad = {self.C/self.A/2:.2f}  ->  ({self.C/self.A/2:.2f})² = {(self.C/self.A/2)**2:.2f}\n\n"
                texto += f"Paso 3: FORMA CANÓNICA (parábola vertical):\n"
                texto += f"   (x {'-' if h>=0 else '+'} {abs(h):.2f})² = {p:.2f}·(y {'-' if k>=0 else '+'} {abs(k):.2f})\n"
            else:
                texto += f"Paso 1: Como A = 0, dejamos y² a la izquierda:\n"
                texto += f"   {self.B:.2f}y² + {self.D:.2f}y = {-self.C:.2f}x {'-' if self.E>=0 else '+'} {abs(self.E):.2f}\n\n"
                texto += f"Paso 2: Factor común {self.B:.2f} y completamos cuadrado en y:\n"
                texto += f"   mitad = {self.D/self.B/2:.2f}  ->  ({self.D/self.B/2:.2f})² = {(self.D/self.B/2)**2:.2f}\n\n"
                texto += f"Paso 3: FORMA CANÓNICA (parábola horizontal):\n"
                texto += f"   (y {'-' if k>=0 else '+'} {abs(k):.2f})² = {p:.2f}·(x {'-' if h>=0 else '+'} {abs(h):.2f})\n"
            texto += f"   Vértice = ({h:.2f}, {k:.2f})\n"

        texto += f"\n>> Clasificación: {self.tipo}."
        return texto

    def paso_a_paso_inverso(self):
        c = self.forma_canonica()
        texto = "=== PROCEDIMIENTO INVERSO (CANÓNICA -> GENERAL) ===\n\n"

        if self.tipo in ["Circunferencia", "Elipse", "Hipérbola"]:
            h, k = c["h"], c["k"]
            texto += f"Partimos de la canónica con centro ({h:.2f}, {k:.2f}).\n\n"
            texto += f"Paso 1: Expandimos los binomios:\n"
            texto += f"   (x {'-' if h>=0 else '+'} {abs(h):.2f})² = x² {'-' if h>=0 else '+'} {abs(2*h):.2f}x + {h**2:.2f}\n"
            texto += f"   (y {'-' if k>=0 else '+'} {abs(k):.2f})² = y² {'-' if k>=0 else '+'} {abs(2*k):.2f}y + {k**2:.2f}\n\n"
            texto += f"Paso 2: Multiplicamos por sus coeficientes A={self.A:.2f} y B={self.B:.2f}.\n"
            texto += f"Paso 3: Pasamos todo a la izquierda e igualamos a 0.\n"
            texto += f"Paso 4: Sumando los términos sueltos recuperamos la general:\n"
            texto += f"   {self.ecuacion_general_str()}\n"
        else:
            h, k, p = c["h"], c["k"], c["p"]
            if c["orientacion"] == "vertical":
                texto += f"Partimos de (x {'-' if h>=0 else '+'} {abs(h):.2f})² = {p:.2f}(y {'-' if k>=0 else '+'} {abs(k):.2f}).\n\n"
                texto += f"Paso 1: Expandimos: x² {'-' if h>=0 else '+'} {abs(2*h):.2f}x + {h**2:.2f} = {p:.2f}y {'-' if k>=0 else '+'} {abs(p*k):.2f}\n"
            else:
                texto += f"Partimos de (y {'-' if k>=0 else '+'} {abs(k):.2f})² = {p:.2f}(x {'-' if h>=0 else '+'} {abs(h):.2f}).\n\n"
                texto += f"Paso 1: Expandimos: y² {'-' if k>=0 else '+'} {abs(2*k):.2f}y + {k**2:.2f} = {p:.2f}x {'-' if h>=0 else '+'} {abs(p*h):.2f}\n"
            texto += f"Paso 2: Multiplicamos por el coeficiente principal y pasamos todo a la izquierda.\n"
            texto += f"Paso 3: Igualando a 0 recuperamos la general:\n"
            texto += f"   {self.ecuacion_general_str()}\n"
        return texto

    def sacar_coordenadas(self, n=900):
        """
        Genera las coordenadas (x, y) de la cónica.

        La ventana de barrido se calcula a partir de la forma canónica
        (centro y semiejes reales), de modo que el gráfico quede siempre
        centrado, bien muestreado y a escala, sin importar el RUT.

        Si la cónica no tiene puntos reales (cónica imaginaria), se marca
        self.es_real = False y se retorna lista vacía.
        """
        self.es_real = True
        self.mensaje = ""
        puntos = []

        # --- PARÁBOLA DE EJE HORIZONTAL (no hay término x²) ---
        if self.A == 0:
            # By² + Cx + Dy + E = 0  ->  x = -(By² + Dy + E) / C
            k = -self.D / (2 * self.B)          # 'y' del vértice
            ancho = self._ancho_parabola()      # cuánto abrir alrededor del vértice
            y0, y1 = k - ancho, k + ancho
            paso = (y1 - y0) / n
            for i in range(n + 1):
                y = y0 + i * paso
                x = -(self.B * (y ** 2) + self.D * y + self.E) / self.C
                puntos.append((x, y))

        # --- PARÁBOLA DE EJE VERTICAL (no hay término y²) ---
        elif self.B == 0:
            # Ax² + Cx + Dy + E = 0  ->  y = -(Ax² + Cx + E) / D
            h = -self.C / (2 * self.A)
            ancho = self._ancho_parabola()
            x0, x1 = h - ancho, h + ancho
            paso = (x1 - x0) / n
            for i in range(n + 1):
                x = x0 + i * paso
                y = -(self.A * (x ** 2) + self.C * x + self.E) / self.D
                puntos.append((x, y))

        # --- CENTRALES: CIRCUNFERENCIA, ELIPSE, HIPÉRBOLA ---
        else:
            h = -self.C / (2 * self.A)
            k = -self.D / (2 * self.B)
            # Completación de cuadrados:  A(x-h)² + B(y-k)² = M
            M = self.A * h ** 2 + self.B * k ** 2 - self.E

            mismo_signo = (self.A * self.B) > 0

            if mismo_signo:
                # Circunferencia / Elipse. Real solo si M/A > 0
                if (M / self.A) <= 0:
                    self.es_real = False
                    self.mensaje = ("La cónica no posee puntos reales "
                                    "(cónica imaginaria). Prueba con otro RUT.")
                    return []
                semi_x = (M / self.A) ** 0.5     # semieje en x
                x0, x1 = h - semi_x, h + semi_x  # barrido exacto extremo a extremo
            else:
                # Hipérbola: mostramos ~3 semiejes a cada lado del centro
                semi_x = (abs(M / self.A)) ** 0.5 if M != 0 else 1.0
                if semi_x == 0:
                    semi_x = 1.0
                x0, x1 = h - 3 * semi_x, h + 3 * semi_x

            paso = (x1 - x0) / n
            a_coef = self.B
            b_coef = self.D
            for i in range(n + 1):
                x = x0 + i * paso
                c_coef = self.A * (x ** 2) + self.C * x + self.E
                disc = b_coef ** 2 - 4 * a_coef * c_coef
                if disc < 0:
                    continue
                raiz = disc ** 0.5
                puntos.append((x, (-b_coef + raiz) / (2 * a_coef)))
                puntos.append((x, (-b_coef - raiz) / (2 * a_coef)))

        return puntos

    def _ancho_parabola(self):
        """Semiancho razonable para abrir la parábola alrededor del vértice."""
        if self.A == 0:
            base = abs(self.C / self.B) if self.B != 0 else 1.0
        else:
            base = abs(self.D / self.A) if self.A != 0 else 1.0
        ancho = base * 1.5
        if ancho < 5:
            ancho = 5.0
        if ancho > 20:
            ancho = 20.0
        return ancho