#!/usr/bin/env python3
import curses
import random
import time

# Frames de aleteo para los murciélagos (ASCII Art)
BAT_FRAMES = [
    [
        r" / \^/ \ ",
        r"(   v   )"
    ],
    [
        r"  /--- \ ",
        r" (  v   )"
    ],
    [
        r" \_/^\_/ ",
        r"  ( v )  "
    ]
]

MANSION_ART = [
    r"                   /|                     ",
    r"                  / |  /\                 ",
    r"                 /__| /  \                ",
    r"                |  _ | |  |   _|_         ",
    r"                | | || |  |  |   |        ",
    r"  ______________|_|_||_|__|__|___|______  ",
    r" /                                      \ ",
    r"/________________________________________\\"
]

MOON_ART = [
    r"  .-'''-.  ",
    r" /   _   \ ",
    r"|   ( )   |",
    r" \   '-' / ",
    r"  '-...-'  "
]

class Bat:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.reset()

    def reset(self):
        self.x = float(self.max_x - 1)
        # Mantener los murciélagos en el tercio superior/medio
        self.y = float(random.randint(2, max(3, self.max_y - 12)))
        self.speed = random.uniform(0.6, 1.2)
        self.frame = random.randint(0, len(BAT_FRAMES) - 1)

    def update(self):
        self.x -= self.speed
        self.frame = (self.frame + 1) % len(BAT_FRAMES)
        if self.x < -10:
            self.reset()

    def draw(self, stdscr, attr):
        current_frame = BAT_FRAMES[self.frame]
        for idx, line in enumerate(current_frame):
            draw_y = int(self.y) + idx
            draw_x = int(self.x)
            if 0 <= draw_y < self.max_y:
                # Dibujar solo las partes visibles dentro de los límites
                if draw_x < self.max_x and draw_x + len(line) > 0:
                    valid_line = line
                    start_char = 0
                    if draw_x < 0:
                        start_char = abs(draw_x)
                        valid_line = line[start_char:]
                        draw_x = 0
                    try:
                        stdscr.addstr(draw_y, draw_x, valid_line[:self.max_x - draw_x], attr)
                    except curses.error:
                        pass

def draw_background(stdscr, max_y, max_x, stars, color_magenta, color_yellow):
    # 1. Dibujar estrellas
    for sy, sx in stars:
        if random.random() < 0.1: # Titileo
            try:
                stdscr.addch(sy, sx, '.', color_yellow)
            except curses.error:
                pass
        else:
            try:
                stdscr.addch(sy, sx, '*', color_magenta)
            except curses.error:
                pass

    # 2. Dibujar Luna (arriba a la derecha)
    moon_x = max_x - 16
    moon_y = 1
    if moon_x > 0 and max_y > 8:
        for idx, line in enumerate(MOON_ART):
            if moon_y + idx < max_y:
                try:
                    stdscr.addstr(moon_y + idx, moon_x, line[:max_x - moon_x], color_yellow | curses.A_BOLD)
                except curses.error:
                    pass

    # 3. Dibujar Silueta de Mansión (abajo al centro/izquierda)
    mansion_y_start = max_y - len(MANSION_ART) - 1
    if mansion_y_start > 0:
        for idx, line in enumerate(MANSION_ART):
            draw_y = mansion_y_start + idx
            if 0 <= draw_y < max_y - 1:
                try:
                    stdscr.addstr(draw_y, 4, line[:max_x - 5], color_magenta)
                except curses.error:
                    pass

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.use_default_colors()

    # Definición de parejas de color
    curses.init_pair(1, curses.COLOR_MAGENTA, -1) # Tono gótico nocturno
    curses.init_pair(2, curses.COLOR_YELLOW, -1)  # Luna y destellos
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE) # Relámpago (Invertido)

    COLOR_GOTHIC = curses.color_pair(1)
    COLOR_MOON = curses.color_pair(2)
    COLOR_FLASH = curses.color_pair(3)

    max_y, max_x = stdscr.getmaxyx()

    # Generar posiciones de estrellas fijas
    stars = [(random.randint(1, max_y - 10), random.randint(1, max_x - 2)) for _ in range(25)]

    # Inicializar murciélagos
    bats = [Bat(max_x, max_y) for _ in range(4)]

    flash_timer = 0

    while True:
        # Detectar redimensionamiento de pantalla
        new_y, new_x = stdscr.getmaxyx()
        if new_y != max_y or new_x != max_x:
            max_y, max_x = new_y, new_x
            stars = [(random.randint(1, max_y - 10), random.randint(1, max_x - 2)) for _ in range(25)]
            for b in bats:
                b.max_x = max_x
                b.max_y = max_y

        stdscr.erase()

        # Posibilidad de relámpago (3% por frame)
        is_flash = False
        if flash_timer > 0:
            flash_timer -= 1
            is_flash = True
        elif random.random() < 0.03:
            flash_timer = random.randint(1, 2) # Duración del destello
            is_flash = True

        if is_flash:
            stdscr.bkgd(' ', COLOR_FLASH)
            current_bat_attr = COLOR_FLASH
        else:
            stdscr.bkgd(' ', curses.color_pair(0))
            draw_background(stdscr, max_y, max_x, stars, COLOR_GOTHIC, COLOR_MOON)
            current_bat_attr = COLOR_GOTHIC | curses.A_BOLD

        # Actualizar y dibujar murciélagos
        for bat in bats:
            if not is_flash:
                bat.update()
            bat.draw(stdscr, current_bat_attr)

        stdscr.refresh()

        # Salir si el usuario presiona cualquier tecla
        if stdscr.getch() != -1:
            break

        time.sleep(0.08)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
