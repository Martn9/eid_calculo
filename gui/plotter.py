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

def dibujar_limites(frame_destino, x_vals, y_vals, x_hueco=None, y_hueco=None,
                    asintota_x=None, titulo="Función por Tramos"):
    """
    Dibuja la función por tramos.
    - x_hueco/y_hueco: círculo vacío para la discontinuidad removible.
    - asintota_x: dibuja la asíntota vertical (caso discontinuidad infinita)
      y separa las ramas izquierda/derecha para que no se una el salto al infinito.
    """
    fig, ax = plt.subplots(figsize=(6, 5))

    if asintota_x is not None:
        # Separar en dos ramas para no dibujar la línea vertical falsa
        xi = [x for x in x_vals if x < asintota_x]
        yi = y_vals[:len(xi)]
        xd = x_vals[len(xi):]
        yd = y_vals[len(xi):]
        ax.plot(xi, yi, color="#1f538d", linewidth=2)
        ax.plot(xd, yd, color="#1f538d", linewidth=2)
        ax.axvline(asintota_x, color="red", linestyle="--", linewidth=1.5, label="Asíntota vertical")
        ax.set_ylim(-50, 50)  # recorte para apreciar la tendencia al infinito
        ax.legend(loc="upper right", fontsize=8)
    else:
        ax.plot(x_vals, y_vals, color="#1f538d", linewidth=2)

    # Círculo vacío (ruptura) para discontinuidad removible
    if x_hueco is not None and y_hueco is not None:
        ax.plot(x_hueco, y_hueco, marker='o', markerfacecolor='white',
                markeredgecolor='red', markersize=9, zorder=5)

    ax.set_title(titulo)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)

    _preparar_canvas(frame_destino, fig)

def dibujar_conica(frame_destino, x_vals, y_vals, titulo="Sección Cónica"):
    """Dibuja la cónica SOLO utilizando los puntos recibidos (según rúbrica)."""
    fig, ax = plt.subplots(figsize=(6, 5))

    ax.scatter(x_vals, y_vals, color="#8d1f2b", s=6)

    # Autoescalado: encuadramos la cónica con un margen del 12%
    if x_vals and y_vals:
        min_x, max_x = min(x_vals), max(x_vals)
        min_y, max_y = min(y_vals), max(y_vals)
        mx = (max_x - min_x) * 0.12 or 1
        my = (max_y - min_y) * 0.12 or 1
        ax.set_xlim(min_x - mx, max_x + mx)
        ax.set_ylim(min_y - my, max_y + my)

    ax.set_title(titulo)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_aspect('equal', adjustable='datalim')  # circunferencias redondas, sin distorsión

    _preparar_canvas(frame_destino, fig)


def mostrar_mensaje(frame_destino, texto):
    """Muestra un mensaje en el área de gráfico (ej. cónica imaginaria)."""
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.text(0.5, 0.5, texto, ha="center", va="center", wrap=True, fontsize=12)
    ax.axis("off")
    _preparar_canvas(frame_destino, fig)