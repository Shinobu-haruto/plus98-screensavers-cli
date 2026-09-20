#!/usr/bin/env python3
import curses
import random
import time

FISH_PATTERNS = [
    {
        "left": [r"<='|||<"],
        "right": [r">|||='>"],
        "width": 7, "height": 1, "color_pair": 2
    },
    {
        "left": [r"  /\\", r"<=={>", r"  \\/"],
        "right": [r"  /\\", r"<}==>", r"  \\/"],
        "width": 6, "height": 3, "color_pair": 3
    },
    {
        "left": [r"  ,-. ", r"<=( °>", r"  `-' "],
        "right": [r" .-.  ", r"<° )=>", r" `-'  "],
        "width": 6, "height": 3, "color_pair": 4
    },
    {
        "left": [r"<\"><"],
        "right": [r"><\">"],
        "width": 4, "height": 1, "color_pair": 3
    }
]

CORAL_ART = [
    r"   (   )      )(     (   ) ",
    r"  (     )    (  )   (     )",
    r" /~~~~~~~\  /~~~~\ /~~~~~~~\\"
]

class Fish:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.reset()

    def reset(self):
        self.type = random.choice(FISH_PATTERNS)
        self.direction = random.choice(["left", "right"])
        self.speed = random.uniform(0.4, 1.1)
        self.y = float(random.randint(3, max(4, self.max_y - 5)))
        
        if self.direction == "left":
            self.x = float(self.max_x + random.randint(1, 10))
        else:
            self.x = float(-self.type["width"] - random.randint(1, 10))

    def update(self):
        if self.direction == "left":
            self.x -= self.speed
            if self.x < -self.type["width"]:
                self.reset()
        else:
            self.x += self.speed
            if self.x > self.max_x + self.type["width"]:
                self.reset()

    def draw(self, stdscr):
        lines = self.type[self.direction]
        color = curses.color_pair(self.type["color_pair"]) | curses.A_BOLD
        
        for idx, line in enumerate(lines):
            draw_y = int(self.y) + idx
            draw_x = int(self.x)
            
            if 0 <= draw_y < self.max_y:
                # Filtrar salida parcial fuera de los bordes laterales
                if draw_x < self.max_x and draw_x + len(line) > 0:
                    valid_line = line
                    if draw_x < 0:
                        start_char = abs(draw_x)
                        valid_line = line[start_char:]
                        draw_x = 0
                    try:
                        stdscr.addstr(draw_y, draw_x, valid_line[:self.max_x - draw_x], color)
                    except curses.error:
                        pass

class Bubble:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.reset()

    def reset(self):
        self.x = float(random.randint(2, max(3, self.max_x - 3)))
        self.y = float(self.max_y - 2)
        self.speed = random.uniform(0.3, 0.7)
        self.char = random.choice(['o', 'O', '.', '°'])

    def update(self):
        self.y -= self.speed
        # Ligera oscilación horizontal
        self.x += random.choice([-0.2, 0.0, 0.2])
        if self.y <= 1:
            self.reset()

    def draw(self, stdscr, color_cyan):
        draw_y = int(self.y)
        draw_x = int(self.x)
        if 0 <= draw_y < self.max_y and 0 <= draw_x < self.max_x:
            try:
                stdscr.addch(draw_y, draw_x, self.char, color_cyan)
            except curses.error:
                pass

def draw_environment(stdscr, max_y, max_x, color_blue, color_cyan, color_green):
    # 1. Superficie / Rayos de luz en la parte superior
    surface_wave = "~" * max_x
    try:
        stdscr.addstr(0, 0, surface_wave, color_cyan | curses.A_BOLD)
    except curses.error:
        pass

    # Rayos de luz que bajan
    for x in range(2, max_x - 2, 8):
        for y in range(1, min(6, max_y)):
            if (x + y) % 3 == 0:
                try:
                    stdscr.addch(y, x + (y // 2), '\\', color_cyan)
                except curses.error:
                    pass

    # 2. Arrecifes/Algas en el fondo
    coral_start_y = max_y - len(CORAL_ART)
    if coral_start_y > 2:
        for idx, line in enumerate(CORAL_ART):
            draw_y = coral_start_y + idx
            if 0 <= draw_y < max_y:
                # Repetir el patrón a lo largo del fondo
                repeated_line = (line * ((max_x // len(line)) + 2))[:max_x]
                try:
                    stdscr.addstr(draw_y, 0, repeated_line, color_green)
                except curses.error:
                    pass

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.use_default_colors()

    # Parejas de color marinas
    curses.init_pair(1, curses.COLOR_BLUE, -1)    # Agua / Fondo
    curses.init_pair(2, curses.COLOR_YELLOW, -1)  # Pez Dorado/Amarillo
    curses.init_pair(3, curses.COLOR_RED, -1)     # Pez Rojo/Naranja
    curses.init_pair(4, curses.COLOR_CYAN, -1)    # Burbujas / Superficie
    curses.init_pair(5, curses.COLOR_GREEN, -1)   # Algas / Corales

    COLOR_CYAN = curses.color_pair(4) | curses.A_BOLD
    COLOR_BLUE = curses.color_pair(1)
    COLOR_GREEN = curses.color_pair(5)

    max_y, max_x = stdscr.getmaxyx()

    # Inicializar objetos
    fishes = [Fish(max_x, max_y) for _ in range(6)]
    bubbles = [Bubble(max_x, max_y) for _ in range(12)]

    while True:
        new_y, new_x = stdscr.getmaxyx()
        if new_y != max_y or new_x != max_x:
            max_y, max_x = new_y, new_x
            for f in fishes:
                f.max_x = max_x
                f.max_y = max_y
            for b in bubbles:
                b.max_x = max_x
                b.max_y = max_y

        stdscr.erase()

        # Dibujar entorno acuático
        draw_environment(stdscr, max_y, max_x, COLOR_BLUE, COLOR_CYAN, COLOR_GREEN)

        # Actualizar y dibujar burbujas
        for bubble in bubbles:
            bubble.update()
            bubble.draw(stdscr, COLOR_CYAN)

        # Actualizar y dibujar peces
        for fish in fishes:
            fish.update()
            fish.draw(stdscr)

        stdscr.refresh()

        # Salir al presionar cualquier tecla
        if stdscr.getch() != -1:
            break

        time.sleep(0.08)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
