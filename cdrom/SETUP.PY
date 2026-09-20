#!/usr/bin/env python3
import curses
import time
import sys
import os

COMPONENTS = [
    ("Mystery (Casa Embrujada)", True),
    ("Underwater (Bajo el Agua)", True),
    ("Inside Your Computer (Circuito PCB)", True),
    ("Space (Viaje Espacial 3D)", True),
]

FILES = [
    "PLUS98/SYSTEM/MYSTERY.PY",
    "PLUS98/SYSTEM/UNDERWATER.PY",
    "PLUS98/SYSTEM/INSIDE_COMPUTER.PY",
    "PLUS98/SYSTEM/SPACE.PY",
    "PLUS98/DRIVERS/CURSES_ENGINE.DLL",
    "PLUS98/THEMES/MYSTERY.THEME",
    "PLUS98/THEMES/UNDERWATER.THEME",
    "PLUS98/THEMES/COMPUTER.THEME",
    "PLUS98/THEMES/SPACE.THEME",
    "PLUS98/FONTS/VGA_8X16.FON",
]

def draw_header(stdscr, title):
    max_y, max_x = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(0, 0, " " * max_x)
    stdscr.addstr(0, 2, title)
    stdscr.attroff(curses.color_pair(1) | curses.A_BOLD)

def draw_footer(stdscr, text):
    max_y, max_x = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(max_y - 1, 0, " " * max_x)
    stdscr.addstr(max_y - 1, 2, text)
    stdscr.attroff(curses.color_pair(1))

def draw_dialog(stdscr, y, x, height, width, title):
    # Sombra del cuadro de diálogo estilo retro
    for row in range(1, height + 1):
        if y + row < stdscr.getmaxyx()[0] and x + width < stdscr.getmaxyx()[1]:
            stdscr.addstr(y + row, x + width, "  ", curses.color_pair(3))
    
    # Cuadro principal blanco/gris
    for h in range(height):
        stdscr.addstr(y + h, x, " " * width, curses.color_pair(2))
    
    # Borde superior del diálogo
    stdscr.addstr(y, x, "┌" + "─" * (width - 2) + "┐", curses.color_pair(2))
    for h in range(1, height - 1):
        stdscr.addstr(y + h, x, "│", curses.color_pair(2))
        stdscr.addstr(y + h, x + width - 1, "│", curses.color_pair(2))
    stdscr.addstr(y + height - 1, x, "└" + "─" * (width - 2) + "┘", curses.color_pair(2))
    
    # Título del cuadro
    stdscr.addstr(y, x + 2, f" {title} ", curses.color_pair(2) | curses.A_BOLD)

def setup_wizard(stdscr):
    curses.curs_set(0)
    curses.start_color()
    
    # Paleta de colores clásica de Setup
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)   # Fondo e indicador
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)   # Ventanas
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)  # Sombras
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLUE)  # Destacado
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_DARKGRAY if hasattr(curses, 'COLOR_DARKGRAY') else curses.COLOR_BLACK)

    stdscr.bkgd(' ', curses.color_pair(1))
    
    # PASO 1: Bienvenida
    while True:
        stdscr.erase()
        draw_header(stdscr, "Instalación de Microsoft Plus! 98 para Linux Terminal")
        draw_footer(stdscr, "<Enter> Continuar  |  <Esc> Cancelar")

        max_y, max_x = stdscr.getmaxyx()
        h, w = 12, 60
        y, x = (max_y - h) // 2, (max_x - w) // 2
        
        draw_dialog(stdscr, y, x, h, w, "Bienvenido al Asistente de Instalación")
        
        stdscr.addstr(y + 2, x + 4, "Bienvenido a la instalación de Plus! 98.", curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(y + 4, x + 4, "Este programa instalará los salvapantallas retro", curses.color_pair(2))
        stdscr.addstr(y + 5, x + 4, "en tu entorno de terminal.", curses.color_pair(2))
        stdscr.addstr(y + 7, x + 4, "Presione ENTER para comenzar la instalación.", curses.color_pair(2))

        # Botón
        stdscr.addstr(y + 9, x + 22, "[  Aceptar  ]", curses.color_pair(1) | curses.A_BOLD)
        
        stdscr.refresh()
        key = stdscr.getch()
        if key in [10, 13]: # Enter
            break
        elif key == 27: # Esc
            return False

    # PASO 2: Copiado / Progreso
    stdscr.erase()
    draw_header(stdscr, "Instalación de Microsoft Plus! 98 - Copiando archivos...")
    draw_footer(stdscr, "Por favor espere mientras se completan los archivos...")

    h, w = 10, 64
    y, x = (max_y - h) // 2, (max_x - w) // 2
    draw_dialog(stdscr, y, x, h, w, "Copiando componentes...")

    for i, file_path in enumerate(FILES):
        stdscr.addstr(y + 2, x + 4, f"Instalando: {file_path}".ljust(54), curses.color_pair(2))
        
        # Porcentaje y Barra
        percent = int(((i + 1) / len(FILES)) * 100)
        bar_width = 50
        filled = int((bar_width * percent) / 100)
        bar = "█" * filled + "░" * (bar_width - filled)
        
        stdscr.addstr(y + 4, x + 4, f"Progreso: [{bar}] {percent}%", curses.color_pair(2))
        stdscr.refresh()
        time.sleep(0.25)

    # PASO 3: Finalización
    stdscr.erase()
    draw_header(stdscr, "Instalación de Microsoft Plus! 98 - Completada")
    draw_footer(stdscr, "<Enter> Finalizar")

    draw_dialog(stdscr, y, x, h, w, "Instalación Finalizada")
    stdscr.addstr(y + 2, x + 4, "¡La instalación se ha completado con éxito!", curses.color_pair(2) | curses.A_BOLD)
    stdscr.addstr(y + 4, x + 4, "Ya puedes ejecutar el comando ./plus98.py o", curses.color_pair(2))
    stdscr.addstr(y + 5, x + 4, "seleccionar tus temas desde la línea de comandos.", curses.color_pair(2))
    stdscr.addstr(y + 7, x + 22, "[  Finalizar  ]", curses.color_pair(1) | curses.A_BOLD)

    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key in [10, 13, 27]:
            break

    return True

def main():
    try:
        curses.wrapper(setup_wizard)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
