import customtkinter as ctk
import sys
import os

# Agregamos la ruta principal para importar módulos lógicos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import rut_validacion
from core.limites import Limites
from gui import plotter

class AppWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MAT1186 - Análisis de Cónicas y Límites")
        self.geometry("1000x750")

        # Configuración de las Pestañas
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.tab_rut = self.tabview.add("Validación de RUT")
        self.tab_conicas = self.tabview.add("Secciones Cónicas")
        self.tab_limites = self.tabview.add("Límites")

        # Iniciar la configuración de cada pestaña
        self.setup_rut_tab()
        self.setup_limites_tab()

    def setup_rut_tab(self):
        self.lbl_instruccion = ctk.CTkLabel(self.tab_rut, text="Ingresa el RUT del líder para iniciar:", font=("Arial", 16, "bold"))
        self.lbl_instruccion.pack(pady=10)

        self.entry_rut = ctk.CTkEntry(self.tab_rut, width=250, placeholder_text="12.345.678-9")
        self.entry_rut.pack(pady=10)

        self.btn_validar = ctk.CTkButton(self.tab_rut, text="Validar y Procesar", command=self.validar_rut_gui)
        self.btn_validar.pack(pady=10)

        self.textbox_resultado = ctk.CTkTextbox(self.tab_rut, width=700, height=400, font=("Consolas", 14))
        self.textbox_resultado.pack(pady=10)

    def setup_limites_tab(self):
        """Maquetación de la pestaña de Límites con campos para la defensa oral"""
        # Contenedor principal dividido en Izquierda (Datos/Inputs) y Derecha (Gráfico)
        self.frame_izq = ctk.CTkFrame(self.tab_limites)
        self.frame_izq.pack(side="left", fill="y", padx=10, pady=10)
        
        self.frame_der = ctk.CTkFrame(self.tab_limites, width=500)
        self.frame_der.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # --- PANEL IZQUIERDO: Tablas e Inputs ---
        lbl_titulo = ctk.CTkLabel(self.frame_izq, text="Análisis de Discontinuidad", font=("Arial", 16, "bold"))
        lbl_titulo.pack(pady=10)

        # Caja de texto para mostrar la evidencia computacional (Tabla de valores)
        ctk.CTkLabel(self.frame_izq, text="Evidencia Computacional (Tabla):").pack()
        self.textbox_tabla = ctk.CTkTextbox(self.frame_izq, width=300, height=150, font=("Consolas", 12))
        self.textbox_tabla.pack(pady=5)

        # Campos VACÍOS obligatorios para la defensa oral (Rúbrica)
        ctk.CTkLabel(self.frame_izq, text="--- PARA COMPLETAR EN DEFENSA ---", text_color="yellow").pack(pady=10)
        
        self.entry_lim_izq = ctk.CTkEntry(self.frame_izq, width=200, placeholder_text="Límite por Izquierda")
        self.entry_lim_izq.pack(pady=5)
        
        self.entry_lim_der = ctk.CTkEntry(self.frame_izq, width=200, placeholder_text="Límite por Derecha")
        self.entry_lim_der.pack(pady=5)
        
        self.entry_tipo_disc = ctk.CTkEntry(self.frame_izq, width=200, placeholder_text="Tipo de Discontinuidad")
        self.entry_tipo_disc.pack(pady=5)

    def validar_rut_gui(self):
        """Controlador Principal: Conecta validación con cálculos matemáticos"""
        rut_input = self.entry_rut.get()
        datos = rut_validacion.validar_rut(rut_input)

        self.textbox_resultado.delete("0.0", "end")
        
        if "error" in datos and not datos.get("texto_procedimiento"):
             self.textbox_resultado.insert("0.0", datos["error"])
             return

        # 1. Mostrar texto de validación
        self.textbox_resultado.insert("0.0", datos["texto_procedimiento"])

        if datos["es_valido"]:
            # 2. Si el RUT es válido, procesamos los límites automáticamente
            digitos = datos["digitos"]
            
            # Instanciar la lógica de límites que hizo Martin H.
            analisis = Limites(digitos)
            tabla_val = analisis.tabla_valores()
            coordenadas = analisis.sacar_coordenadas()
            
            # 3. Actualizar la pestaña de límites
            self.actualizar_pestaña_limites(tabla_val, coordenadas)

    def actualizar_pestaña_limites(self, tabla_val, coordenadas):
        """Inyecta los datos matemáticos en la GUI y manda a dibujar"""
        # Formatear la tabla de valores para la vista
        texto_tabla = "x \t\t f(x)\n"
        texto_tabla += "-"*30 + "\n"
        texto_tabla += "Por la Izquierda:\n"
        for x, y in tabla_val["izq"]:
            texto_tabla += f"{x} \t {y}\n"
            
        texto_tabla += "\nPor la Derecha:\n"
        for x, y in tabla_val["der"]:
            texto_tabla += f"{x} \t {y}\n"
            
        self.textbox_tabla.delete("0.0", "end")
        self.textbox_tabla.insert("0.0", texto_tabla)

        # Separar coordenadas (x, y) para enviarlas a matplotlib
        x_vals = [p[0] for p in coordenadas]
        y_vals = [p[1] for p in coordenadas]
        
        # Llamar a plotter.py para que dibuje en el frame derecho
        plotter.dibujar_grafico(self.frame_der, x_vals, y_vals, titulo="Gráfica de la Función por Tramos")