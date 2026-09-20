#!/usr/bin/env python3
import sys
import os
import random
import curses

# Asegurar que reconozca los módulos dentro de src/
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from src import mystery, underwater, inside_computer, space

SCREENSAVERS = {
    "1": ("Mystery (Casa Embrujada)", mystery.main),
    "2": ("Underwater (Bajo el Agua)", underwater.main),
    "3": ("Inside Your Computer (Circuito PCB)", inside_computer.main),
    "4": ("Space (Viaje Espacial 3D)", space.main),
}

def show_menu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    
    selected_idx = 0
    options = list(SCREENSAVERS.values()) + [("Aleatorio (Random)", None), ("Salir", None)]

    while True:
        stdscr.erase()
        max_y, max_x = stdscr.getmaxyx()

        title = "=== Plus! 98 Terminal Screensavers ==="
        stdscr.addstr(2, max(0, (max_x - len(title)) // 2), title, curses.color_pair(1) | curses.A_BOLD)
        stdscr.addstr(3, max(0, (max_x - 32) // 2), "Selecciona un salvapantallas:", curses.A_DIM)

        for idx, (label, _) in enumerate(options):
            y = 6 + idx
            x = max(0, (max_x - len(label) - 4) // 2)
            if idx == selected_idx:
                stdscr.addstr(y, x, f"> {label} <", curses.A_REVERSE | curses.A_BOLD)
            else:
                stdscr.addstr(y, x, f"  {label}  ")

        stdscr.refresh()
        key = stdscr.getch()

        if key in [curses.KEY_UP, ord('k')]:
            selected_idx = (selected_idx - 1) % len(options)
        elif key in [curses.KEY_DOWN, ord('j')]:
            selected_idx = (selected_idx + 1) % len(options)
        elif key in [10, 13]: # Enter
            if selected_idx == len(options) - 1: # Salir
                return None
            elif selected_idx == len(options) - 2: # Aleatorio
                return random.choice([func for _, func in SCREENSAVERS.values()])
            else:
                return options[selected_idx][1]

def print_help():
    print("Uso: plus98 [OPCIÓN]")
    print("\nOpciones disponibles:")
    print("  mystery        Lanza el tema Mystery")
    print("  underwater     Lanza el tema Underwater")
    print("  computer       Lanza el tema Inside Your Computer")
    print("  space          Lanza el tema Space")
    print("  random         Lanza uno al azar")
    print("  --help         Muestra esta ayuda\n")

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["mystery", "1"]:
            curses.wrapper(mystery.main)
        elif arg in ["underwater", "2"]:
            curses.wrapper(underwater.main)
        elif arg in ["computer", "inside_computer", "3"]:
            curses.wrapper(inside_computer.main)
        elif arg in ["space", "4"]:
            curses.wrapper(space.main)
        elif arg in ["random", "rand"]:
            selected = random.choice(list(SCREENSAVERS.values()))[1]
            curses.wrapper(selected)
        else:
            print_help()
    else:
        target_func = curses.wrapper(show_menu)
        if target_func:
            curses.wrapper(target_func)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass