# 🖥️ Plus! 98 Terminal Screensavers

Una reimaginación técnica y nostalgia pura: los clásicos salvapantallas del paquete **Microsoft Plus! 98** reescritos desde cero para la terminal de Linux utilizando exclusivamente **Python 3** y la biblioteca estándar **`curses`**.

Sin emulación de binarios `.scr`, sin extracción de bitmaps ni audio propietario. Todo el arte, la animación y los efectos tridimensionales son generados de forma matemática y procedural mediante caracteres ASCII/ANSI.

---

## 🎨 Temas Incluidos

| Tema | Descripción | Implementación Técnica |
| :--- | :--- | :--- |
| **Mystery** | Atmósfera gótica de la mansión embrujada. | Renderizado procedural de elementos visuales y texto. |
| **Underwater** | Entorno marino con fauna y movimiento de agua. | Simulación de física de fluidos ligera y flujo de partículas/burbujas. |
| **Inside Your Computer** | Tráfico de datos en una placa de circuito impreso (PCB). | Algoritmos de trazado de rutas (*pathfinding*) e hilos en matriz 2D. |
| **Space** | El clásico viaje estelar a velocidad luz. | Proyección de perspectiva 3D $(x, y, z)$ sobre una matriz de terminal plana. |

---

## 🚀 Características Clave

- **100% Nativo y Liviano:** Construido únicamente con bibliotecas estándar de Python (`curses`, `math`, `random`, `sys`). No requiere dependencias externas de `pip`.
- **Bajo Consumo de Recursos:** Ejecución ultraeficiente en TTY/Terminal pura o emuladores de terminal gráficos.
- **Doble Modo de Uso:** Menú interactivo guiado por teclado o ejecución directa mediante interfaz de línea de comandos (CLI).
- **Código Creado desde Cero:** Respetuoso de los derechos de propiedad intelectual; ideal para ser distribuido libremente bajo licencia de código abierto.

---

## 🛠️ Instalación y Requisitos

### Requisitos
- Python 3.6 o superior.
- Sistema operativo tipo UNIX/Linux (o entornos con soporte `curses` nativo).

### Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/plus98-terminal-screensavers.git](https://github.com/tu-usuario/plus98-terminal-screensavers.git)
cd plus98-terminal-screensavers
