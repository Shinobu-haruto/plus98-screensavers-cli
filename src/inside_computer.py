#!/usr/bin/env python3
import curses
import random
import time

# Dibujos ASCII para componentes estáticos
CPU_ART = [
    r"┌────────────────┐",
    r"│   INTEL / 98   │",
    r"│  MICROPROCESSOR│",
    r"│   [ 100 MHz ]  │",
    r"└────────────────┘"
]

RAM_STICK = [
    r"[■■■■■■■■]",
    r"[■■■■■■■■]"
]

BUS_CHARS = ['─', '│', '┌', '┐', '└', '┘', '┼']

class DataPacket:
    def __init__(self, tracks, max_x, max_y):
        self.tracks = tracks
        self.max_x = max_x
        self.max_y = max_y
        self.reset()

    def reset(self):
        if not self.tracks:
            self.path = []
            return
        # Elegir una pista aleatoria para recorrer
        self.path = random.choice(self.tracks)
        self.step = 0
        self.speed = random.choice([1, 2])
        self.char = random.choice(['1', '0', '■', '▲', '⚡', '░'])
        self.color_pair = random.choice([2, 3, 4]) # Verde, Cyan o Amarillo brillante

    def update(self):
        if not self.path:
            return
        self.step += self.speed
        if self.step >= len(self.path):
            self.reset()

    def draw(self, stdscr):
        if not self.path or self.step >= len(self.path):
            return
        y, x = self.path[self.step]
        if 0 <= y < self.max_y and 0 <= x < self.max_x:
            try:
                stdscr.addch(y, x, self.char, curses.color_pair(self.color_pair) | curses.A_BOLD)
            except curses.error:
                pass

def generate_pcb_tracks(max_y, max_x):
    """ Genera rutas rectilíneas simulando pistas de un circuito impreso """
    tracks = []
    num_tracks = 12
    
    for _ in range(num_tracks):
        track = []
        # Iniciar en un borde aleatorio
        if random.choice([True, False]):
            x = random.randint(2, max_x - 3)
            y = 2 if random.choice([True, False]) else max_y - 3
        else:
            x = 2 if random.choice([True, False]) else max_x - 3
            y = random.randint(2, max_y - 3)
            
        direction = random.choice(['H', 'V'])
        length = random.randint(15, 35)

        for _ in range(length):
            track.append((y, x))
            if direction == 'H':
                x += 1 if x < max_x - 3 else -1
            else:
                y += 1 if y < max_y - 3 else -1

            # Giro de 90 grados ocasional
            if random.random() < 0.15:
                direction = 'V' if direction == 'H' else 'H'

        if len(track) > 5:
            tracks.append(track)
            
    return tracks

def draw_static_components(stdscr, max_y, max_x, color_green, color_cyan, color_yellow):
    # 1. Dibujar CPU en el centro
    cpu_y = max_y // 2 - 2
    cpu_x = max_x // 2 - 9
    if cpu_y > 0 and cpu_x > 0 and cpu_y + len(CPU_ART) < max_y and cpu_x + 18 < max_x:
        for idx, line in enumerate(CPU_ART):
            try:
                stdscr.addstr(cpu_y + idx, cpu_x, line, color_yellow | curses.A_BOLD)
            except curses.error:
                pass

    # 2. Dibujar Módulos de RAM en la esquina superior izquierda
    if max_y > 10 and max_x > 30:
        try:
            stdscr.addstr(2, 4, "BANK 0 [RAM]", color_cyan)
            stdscr.addstr(3, 4, RAM_STICK[0], color_green)
            stdscr.addstr(4, 4, RAM_STICK[1], color_green)
            
            stdscr.addstr(6, 4, "BANK 1 [RAM]", color_cyan)
            stdscr.addstr(7, 4, RAM_STICK[0], color_green)
            stdscr.addstr(8, 4, RAM_STICK[1], color_green)
        except curses.error:
            pass

def draw_tracks(stdscr, tracks, max_y, max_x, color_dark_green):
    """ Renderiza las pistas estáticas de cobre/PCB """
    for track in tracks:
        for idx, (y, x) in enumerate(track):
            if 0 <= y < max_y and 0 <= x < max_x:
                try:
                    # Carácter de pista tenue
                    stdscr.addch(y, x, '·', color_dark_green)
                except curses.error:
                    pass

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.use_default_colors()

    # Esquema de colores PCB / Hardware 90s
    curses.init_pair(1, curses.COLOR_GREEN, -1)   # Pistas y componentes base
    curses.init_pair(2, curses.COLOR_GREEN, -1)   # Datos verde brillante
    curses.init_pair(3, curses.COLOR_CYAN, -1)    # Datos cian/buses
    curses.init_pair(4, curses.COLOR_YELLOW, -1)  # CPU / Alimentación (VCC)

    COLOR_DARK_GREEN = curses.color_pair(1) | curses.A_DIM
    COLOR_GREEN = curses.color_pair(2)
    COLOR_CYAN = curses.color_pair(3)
    COLOR_YELLOW = curses.color_pair(4)

    max_y, max_x = stdscr.getmaxyx()

    tracks = generate_pcb_tracks(max_y, max_x)
    packets = [DataPacket(tracks, max_x, max_y) for _ in range(16)]

    while True:
        new_y, new_x = stdscr.getmaxyx()
        if new_y != max_y or new_x != max_x:
            max_y, max_x = new_y, new_x
            tracks = generate_pcb_tracks(max_y, max_x)
            packets = [DataPacket(tracks, max_x, max_y) for _ in range(16)]

        stdscr.erase()

        # 1. Dibujar fondo de pistas de la placa
        draw_tracks(stdscr, tracks, max_y, max_x, COLOR_DARK_GREEN)

        # 2. Dibujar chips estáticos (CPU / RAM)
        draw_static_components(stdscr, max_y, max_x, COLOR_GREEN, COLOR_CYAN, COLOR_YELLOW)

        # 3. Mover y dibujar los paquetes de datos fluyendo
        for packet in packets:
            packet.update()
            packet.draw(stdscr)

        stdscr.refresh()

        # Salir con cualquier tecla
        if stdscr.getch() != -1:
            break

        time.sleep(0.06)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
