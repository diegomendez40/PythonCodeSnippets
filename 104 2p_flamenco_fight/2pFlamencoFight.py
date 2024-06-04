"""
Flamenco Witches Battle
------------------------
Un juego de batalla de brujas flamencas en las calles de Sevilla.

Autor: diegomendez40 (Diego Méndez Romero)
Fecha: 04/06/2024
"""

import pygame
import os

pygame.font.init()
pygame.mixer.init()

# Configuración del juego
WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
RED = (200, 0, 50)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
FPS = 60
STEP = 3  # Velocidad de movimiento de las brujas
BULLET_SPEED = 5
BULLET_NUM = 5

# Inicializar la ventana del juego
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flamenco Witches Battle")

# Cargar recursos (sonidos, fuentes, imágenes)
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Sounds', 'Fire.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Sounds', 'Hit.mp3'))
HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 50)
FLAMENCO_WITCH_YELLOW = pygame.image.load(os.path.join('Images', 'flamenco_witch_yellow_small.png'))
FLAMENCO_WITCH_BLUE = pygame.image.load(os.path.join('Images', 'flamenco_witch_yellow_small.png'))
SEVILLE_STREET = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'seville_street.png')), (WIDTH, HEIGHT))

# Definir la línea central y eventos personalizados para los impactos de bala
MID_BORDER = pygame.Rect((WIDTH // 2) - 2.5, 0, 5, HEIGHT)
YELLOW_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

# Definición de la clase Player
class Player:
    def __init__(self, x, y, width, height, image, color):
        """
        Inicializa un objeto Player con su posición, dimensiones, imagen y color.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.color = color
        self.health = 100
        self.bullets = []

    def move(self, keys, left_key, right_key, up_key, down_key, boundary_rect=None):
        """
        Mueve al jugador según las teclas presionadas y los límites especificados.
        """
        if keys[left_key] and self.rect.x - STEP > 0:
            self.rect.x -= STEP
        if keys[right_key] and self.rect.x + STEP + self.rect.width < (boundary_rect.x if boundary_rect else WIDTH):
            self.rect.x += STEP
        if keys[up_key] and self.rect.y - STEP > 0:
            self.rect.y -= STEP
        if keys[down_key] and self.rect.y + STEP + self.rect.height < HEIGHT:
            self.rect.y += STEP

    def draw(self, window):
        """
        Dibuja al jugador y sus balas en la ventana especificada.
        """
        window.blit(self.image, (self.rect.x, self.rect.y))
        for bullet in self.bullets:
            pygame.draw.rect(window, self.color, bullet)

    def handle_bullets(self, opponent):
        """
        Maneja el movimiento de las balas y la detección de colisiones con el oponente.
        """
        for bullet in self.bullets:
            bullet.x += BULLET_SPEED if self.color == YELLOW else -BULLET_SPEED
            if opponent.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(BLUE_HIT if self.color == YELLOW else YELLOW_HIT))
                self.bullets.remove(bullet)
            elif bullet.x > WIDTH or bullet.x < 0:
                self.bullets.remove(bullet)

def draw_window(yellow, blue):
    """
    Dibuja la ventana del juego con los elementos del fondo, la línea central, la salud de los jugadores y los jugadores en sí.
    """
    WIN.blit(SEVILLE_STREET, (0, 0))
    pygame.draw.rect(WIN, WHITE, MID_BORDER)
    
    yellow_health_txt = HEALTH_FONT.render("Health: " + str(yellow.health), 1, WHITE)
    blue_health_txt = HEALTH_FONT.render("Health: " + str(blue.health), 1, WHITE)

    WIN.blit(yellow_health_txt, (10, 10))
    WIN.blit(blue_health_txt, (WIDTH - blue_health_txt.get_width() - 10, 10))

    yellow.draw(WIN)
    blue.draw(WIN)
    
    pygame.display.update()

def draw_winner(text):
    """
    Muestra el mensaje del ganador en la pantalla durante 5 segundos.
    """
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

def display_instructions():
    """
    Muestra las instrucciones del juego en la pantalla durante 5 segundos.
    """
    instructions = [
        "Flamenco Witches Battle",
        " ",
        "Controls:",
        "Left player:",
        "W - Up, A - Left, S - Down, D - Right, LCTRL - Fire",
        "Right player:",
        "Arrow keys - Move, RCTRL - Fire",
        " ",
        "Aim at the tip of the hat",
        "to deplete opponent's health and win!"
    ]
    for i, line in enumerate(instructions):
        instruction_text = HEALTH_FONT.render(line, 1, WHITE)
        WIN.blit(instruction_text, (WIDTH / 2 - instruction_text.get_width() / 2, HEIGHT / 2 - 100 + i * 30))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    """
    Función principal del juego que maneja el bucle del juego y la lógica del juego.
    """
    yellow = Player(200, 250, 32, 32, FLAMENCO_WITCH_YELLOW, YELLOW)
    blue = Player(650, 250, 32, 32, FLAMENCO_WITCH_BLUE, BLUE)

    clock = pygame.time.Clock()
    run = True

    # Mostrar las instrucciones al inicio del juego
    display_instructions()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow.bullets) < BULLET_NUM:
                    bullet = pygame.Rect(yellow.rect.x + yellow.rect.width, yellow.rect.y + yellow.rect.height // 2 - 2, 10, 5)
                    yellow.bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(blue.bullets) < BULLET_NUM:
                    bullet = pygame.Rect(blue.rect.x, blue.rect.y + blue.rect.height // 2 - 2, 10, 5)
                    blue.bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow.health -= 10
                BULLET_HIT_SOUND.play()
            if event.type == BLUE_HIT:
                blue.health -= 10
                BULLET_HIT_SOUND.play()
        
        winner_msg = ""
        if yellow.health <= 0:
            winner_msg = "Right-Side Player Wins!"
        if blue.health <= 0:
            winner_msg = "Left-Side Player Wins!"
        if winner_msg != "":
            draw_winner(winner_msg)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow.move(keys_pressed, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, MID_BORDER)
        blue.move(keys_pressed, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN)
        
        yellow.handle_bullets(blue)
        blue.handle_bullets(yellow)
        
        draw_window(yellow, blue)

    main()

if __name__ == "__main__":
    main()