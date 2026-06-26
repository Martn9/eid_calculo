import customtkinter as ctk
import sys
import os

# Agregamos la ruta principal para importar módulos lógicos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import rut_validacion
from core.limites import Limites
from core.conicas import Conica  # Importamos la nueva clase
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
        self.setup_conicas_tab()  # Inicializamos la pestaña de cónicas
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

    def setup_conicas_tab(self):
        """Maquetación de la pestaña de Cónicas con campos vacíos para la defensa oral"""
        self.frame_izq_conicas = ctk.CTkFrame(self.tab_conicas)
        self.frame_izq_conicas.pack(side="left", fill="y", padx=10, pady=10)
        
        self.frame_der_conicas = ctk.CTkFrame(self.tab_conicas, width=500)
        self.frame_der_conicas.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(self.frame_izq_conicas, text="Análisis de Sección Cónica", font=("Arial", 16, "bold")).pack(pady=10)

        # Campos VACÍOS obligatorios para la defensa oral según la rúbrica
        ctk.CTkLabel(self.frame_izq_conicas, text="--- PARA COMPLETAR EN DEFENSA ---", text_color="yellow").pack(pady=10)
        
        self.entry_centro = ctk.CTkEntry(self.frame_izq_conicas, width=250, placeholder_text="Centro (h, k)")
        self.entry_centro.pack(pady=5)
        self.entry_vertices = ctk.CTkEntry(self.frame_izq_conicas, width=250, placeholder_text="Vértices")
        self.entry_vertices.pack(pady=5)
        self.entry_focos = ctk.CTkEntry(self.frame_izq_conicas, width=250, placeholder_text="Focos")
        self.entry_focos.pack(pady=5)
        self.entry_ejes = ctk.CTkEntry(self.frame_izq_conicas, width=250, placeholder_text="Eje Mayor/Menor o Transv./Conj.")
        self.entry_ejes.pack(pady=5)
        self.entry_directriz = ctk.CTkEntry(self.frame_izq_conicas, width=250, placeholder_text="Directriz (si corresponde)")
        self.entry_directriz.pack(pady=5)
        
        ctk.CTkLabel(self.frame_izq_conicas, text="Desarrollo a Canónica:").pack()
        self.textbox_pasos_conica = ctk.CTkTextbox(self.frame_izq_conicas, width=350, height=120, font=("Consolas", 12))
        self.textbox_pasos_conica.pack(pady=2)

        # Cuadro para el procedimiento inverso
        ctk.CTkLabel(self.frame_izq_conicas, text="Procedimiento Inverso (a General):").pack()
        self.textbox_pasos_inverso = ctk.CTkTextbox(self.frame_izq_conicas, width=350, height=120, font=("Consolas", 12))
        self.textbox_pasos_inverso.pack(pady=2)

    def setup_limites_tab(self):
        """Maquetación de la pestaña de Límites con campos para la defensa oral"""
        self.frame_izq = ctk.CTkFrame(self.tab_limites)
        self.frame_izq.pack(side="left", fill="y", padx=10, pady=10)
        
        self.frame_der = ctk.CTkFrame(self.tab_limites, width=500)
        self.frame_der.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        lbl_titulo = ctk.CTkLabel(self.frame_izq, text="Análisis de Discontinuidad", font=("Arial", 16, "bold"))
        lbl_titulo.pack(pady=5)

        # Etiqueta para inyectar la regla de selección automática
        self.lbl_regla_seleccion = ctk.CTkLabel(self.frame_izq, text="Regla de selección: (Esperando validación...)", text_color="cyan")
        self.lbl_regla_seleccion.pack(pady=(0, 10))

        ctk.CTkLabel(self.frame_izq, text="Evidencia Computacional (Tabla):").pack()
        self.textbox_tabla = ctk.CTkTextbox(self.frame_izq, width=300, height=120, font=("Consolas", 12))
        self.textbox_tabla.pack(pady=5)

        # CONEXIÓN: Agregamos una caja oculta/visible para el paso a paso automático del desarrollo matemático
        ctk.CTkLabel(self.frame_izq, text="Procedimiento Algebraico de Límites:").pack()
        self.textbox_desarrollo_auto = ctk.CTkTextbox(self.frame_izq, width=300, height=100, font=("Arial", 11))
        self.textbox_desarrollo_auto.pack(pady=5)

        ctk.CTkLabel(self.frame_izq, text="--- PARA COMPLETAR EN DEFENSA ---", text_color="yellow").pack(pady=5)
        
        # Creación dinámica de campos para la defensa oral
        campos_defensa = [
            "Límite por Izquierda", "Límite por Derecha", 
            "Existencia del Límite", "Valor f(a)", 
            "Conclusión Continuidad", "Tipo de Discontinuidad"
        ]
        self.entradas_limites = {}
        for campo in campos_defensa:
            entry = ctk.CTkEntry(self.frame_izq, width=250, placeholder_text=campo)
            entry.pack(pady=2)
            self.entradas_limites[campo] = entry 
            
        # Campo de texto para justificación escrita requerida por la rúbrica
        self.textbox_justificacion = ctk.CTkTextbox(self.frame_izq, width=250, height=60)
        self.textbox_justificacion.insert("0.0", "Justificación escrita...")
        self.textbox_justificacion.pack(pady=5)

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
            digitos = datos["digitos"]
            
            # --- PROCESAR LÍMITES ---
            analisis = Limites(digitos)
            tabla_val = analisis.tabla_valores()
            coordenadas_lim = analisis.sacar_coordenadas()
            # CONEXIÓN: Le enviamos el objeto 'analisis' completo a la pestaña de límites
            self.actualizar_pestaña_limites(tabla_val, coordenadas_lim, analisis)

            # --- PROCESAR CÓNICAS ---
            dv_limpio = datos["dv"]
            conica = Conica(digitos, dv_limpio)
            self.actualizar_pestaña_conicas(conica)

    def actualizar_pestaña_conicas(self, conica):
        """Inyecta el desarrollo algebraico en la pestaña de Cónicas"""
        self.textbox_pasos_conica.delete("0.0", "end")
        self.textbox_pasos_conica.insert("0.0", conica.paso_a_paso_canonico())
        
        # Preparación para cuando Integrante 1 implemente paso_a_paso_inverso()
        """
        self.textbox_pasos_inverso.delete("0.0", "end")
        self.textbox_pasos_inverso.insert("0.0", conica.paso_a_paso_inverso())
        
        coordenadas = conica.sacar_coordenadas()
        if coordenadas:
            x_vals = [p[0] for p in coordenadas]
            y_vals = [p[1] for p in coordenadas]
            plotter.dibujar_conica(self.frame_der_conicas, x_vals, y_vals, titulo=f"Gráfica: {conica.tipo}")
        """
        
    def actualizar_pestaña_limites(self, tabla_val, coordenadas, analisis):
        """Inyecta los datos matemáticos en la GUI y manda a dibujar"""
        
        # CONEXIÓN: Cada vez que se procese un nuevo RUT, reseteamos a blanco las entradas de la defensa oral
        for entry in self.entradas_limites.values():
            entry.delete(0, "end")
        self.textbox_justificacion.delete("0.0", "end")
        self.textbox_justificacion.insert("0.0", "Justificación escrita...")

        # CONEXIÓN: Inyectamos dinámicamente los textos lógicos automáticos que creamos en limites.py
        self.lbl_regla_seleccion.configure(text=analisis.explicar_regla_seleccion())
        
        self.textbox_desarrollo_auto.delete("0.0", "end")
        self.textbox_desarrollo_auto.insert(
            "0.0", 
            analisis.paso_a_paso_limites() + "\n\n" + analisis.justificar_discontinuidad()
        )

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

        # Filtramos las coordenadas None para evitar errores en matplotlib temporalmente
        x_vals = [p[0] for p in coordenadas if p[1] is not None]
        y_vals = [p[1] for p in coordenadas if p[1] is not None]
        
        plotter.dibujar_limites(self.frame_der, x_vals, y_vals, titulo="Gráfica de la Función por Tramos")

if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()