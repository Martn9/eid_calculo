## Estructura del Proyecto

```text
proyecto_calculo_eid1/
│
├── main.py                  # Punto de entrada de la aplicación. Solo inicializa la GUI.
│
├── core/                    # Aquí va TODA la lógica matemática a mano. CERO librerías externas.
│   ├── __init__.py
│   ├── rut_validator.py     # Lógica del módulo 11 paso a paso.
│   ├── conicas.py           # Generación de coeficientes, clasificación y paso de general a canónica.
│   └── limites.py           # Creación de tramos, cálculo de límites laterales y tipos de discontinuidad.
│
├── gui/                     # Todo lo relacionado con la interfaz visual.
│   ├── __init__.py
│   ├── app_window.py        # Ventana principal, botones y campos de texto.
│   └── plotter.py           # Lógica para dibujar las cónicas y funciones en el plano cartesiano.
│
└── tests/                   # (Opcional pero recomendado)
    └── test_rut.py          # Casos de prueba con RUTs válidos para verificar las 4 cónicas.
