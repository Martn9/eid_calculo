import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def dibujar_grafico(frame_destino, x_vals, y_vals, titulo="Gráfico"):
    """
    Recibe los arreglos x, y desde la carpeta core y los dibuja en la interfaz.
    """
    # Limpiar el frame por si el usuario ingresó otro RUT antes
    for widget in frame_destino.winfo_children():
        widget.destroy()

    # Configurar el plano cartesiano
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(x_vals, y_vals, color="#1f538d", linewidth=2)
    ax.set_title(titulo)
    ax.grid(True, linestyle="--", alpha=0.6)
    
    # Dibujar los ejes X e Y centrales
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    # Incrustar el gráfico en CustomTkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_destino)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)