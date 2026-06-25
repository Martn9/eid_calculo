import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def _preparar_canvas(frame_destino, fig):
    """Función de utilidad (Clean Code) para limpiar memoria y renderizar."""
    for widget in frame_destino.winfo_children():
        widget.destroy()
    plt.close('all') # CRÍTICO: Previene fuga de memoria eliminando figuras ocultas

    canvas = FigureCanvasTkAgg(fig, master=frame_destino)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

def dibujar_limites(frame_destino, x_vals, y_vals, x_hueco=None, y_hueco=None, titulo="Función por Tramos"):
    """Dibuja la función e incluye el círculo vacío si hay discontinuidad removible."""
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Dibujar la línea principal
    ax.plot(x_vals, y_vals, color="#1f538d", linewidth=2)
    
    # Dibujar círculo vacío (ruptura) si el Integrante 2 provee la coordenada
    if x_hueco is not None and y_hueco is not None:
        ax.plot(x_hueco, y_hueco, marker='o', markerfacecolor='white', markeredgecolor='red', markersize=8)

    ax.set_title(titulo)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    _preparar_canvas(frame_destino, fig)

def dibujar_conica(frame_destino, x_vals, y_vals, titulo="Sección Cónica"):
    """Dibuja la cónica SOLO utilizando los puntos recibidos (según rúbrica)."""
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Usamos scatter (puntos) en vez de plot (líneas conectadas)
    ax.scatter(x_vals, y_vals, color="#8d1f2b", s=10) # s es el tamaño del punto
    
    ax.set_title(titulo)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.axis('equal') # CRÍTICO: Para que las circunferencias no se vean como elipses ovaladas

    _preparar_canvas(frame_destino, fig)