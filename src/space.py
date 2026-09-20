#!/usr/bin/env python3
import curses
import random
import time

SHIP_ART = [
    [
        r"   /\   ",
        r"  /  \  ",
        r"=/====\=",
        r"  ||||  "
    ],
    [
        r"  .---.  ",
        r" /  _  \ ",
        r"(  ( )  )",
        r" \  '-' / ",
        r"  '---'  "
    ]
]

ASTEROID_ART = [
    r" .-*-.",
    r"( * * )",
    r" `---'"
]

class Star3D:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.reset()

    def reset(self):
        # Generar coordenadas relativas al centro
        self.x = random.uniform(-self.max_x, self.max_x)
        self.y = random.uniform(-self.max_y, self.max_y)
        self.z = random.uniform(1.0, 20.0)
        self.speed = random.uniform(0.2, 0.5)

    def update(self):
        self.z -= self.speed
        if self.z <= 0.1:
            self.reset()

    def draw(self, stdscr, center_x, center_y, color_cyan, color_white):
        # Proyección perspectiva 3D a 2D
        screen_x = int(center_x + (self.x / self.z))
        screen_y = int(center_y + (self.y / self.z))

        if 0 <= screen_y < self.max_y and 0 <= screen_x < self.max_x:
            # Seleccionar carácter y brillo según la cercanía (z)
            if self.z > 12.0:
                char = '.'
                attr = curses.A_DIM
            elif self.z > 5.0:
                char = '*'
                attr = color_cyan
            else:
                char = 'O'
                attr = color_white | curses.A_BOLD

            try:
                stdscr.addch(screen_y, screen_x, char, attr)
            except curses.error:
                pass

class SpaceObject:
    """ Maneja naves y asteroides atravesando el espacio """
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.reset()

    def reset(self):
        self.is_ship = random.choice([True, False])
        if self.is_ship:
            self.art = random.choice(SHIP_ART)
            self.height = len(self.art)
            self.width = max(len(line) for line in self.art)
            self.color_pair = 3 # Cyan/Amarillo
        else:
            self.art = ASTEROID_ART
            self.height = len(self.art)
            self.width = max(len(line) for line in self.art)
            self.color_pair = 1 # Rojo/Gris

        self.x = float(random.randint(2, max(3, self.max_x - self.width - 2)))
        self.y = float(-self.height - random.randint(1, 10))
        self.speed_y = random.uniform(0.3, 0.7)
        self.speed_x = random.uniform(-0.2, 0.2)

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x
        if self.y > self.max_y + 2:
            self.reset()

    def draw(self, stdscr):
        attr = curses.color_pair(self.color_pair) | curses.A_BOLD
        for idx, line in enumerate(self.art):
            draw_y = int(self.y) + idx
            draw_x = int(self.x)

            if 0 <= draw_y < self.max_y:
                if draw_x < self.max_x and draw_x + len(line) > 0:
                    valid_line = line
                    if draw_x < 0:
                        start_char = abs(draw_x)
                        valid_line = line[start_char:]
                        draw_x = 0
                    try:
                        stdscr.addstr(draw_y, draw_x, valid_line[:self.max_x - draw_x], attr)
                    except curses.error:
                        pass

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.use_default_colors()

    # Esquema de colores espaciales
    curses.init_pair(1, curses.COLOR_RED, -1)     # Asteroides
    curses.init_pair(2, curses.COLOR_CYAN, -1)    # Estrellas intermedias
    curses.init_pair(3, curses.COLOR_YELLOW, -1)  # Naves
    curses.init_pair(4, curses.COLOR_WHITE, -1)   # Estrellas cercanas

    COLOR_CYAN = curses.color_pair(2)
    COLOR_WHITE = curses.color_pair(4)

    max_y, max_x = stdscr.getmaxyx()
    center_x = max_x // 2
    center_y = max_y // 2

    # Inicializar campo de estrellas 3D y objetos
    stars = [Star3D(max_x, max_y) for _ in range(60)]
    space_objects = [SpaceObject(max_x, max_y) for _ in range(2)]

    while True:
        new_y, new_x = stdscr.getmaxyx()
        if new_y != max_y or new_x != max_x:
            max_y, max_x = new_y, new_x
            center_x = max_x // 2
            center_y = max_y // 2
            for s in stars:
                s.max_x = max_x
                s.max_y = max_y
            for obj in space_objects:
                obj.max_x = max_x
                obj.max_y = max_y

        stdscr.erase()

        # 1. Dibujar estrellas en movimiento 3D
        for star in stars:
            star.update()
            star.draw(stdscr, center_x, center_y, COLOR_CYAN, COLOR_WHITE)

        # 2. Dibujar naves/asteroides
        for obj in space_objects:
            obj.update()
            obj.draw(stdscr)

        stdscr.refresh()

        # Salir al presionar cualquier tecla
        if stdscr.getch() != -1:
            break

        time.sleep(0.05)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
