import pygame
import sys

from entities.level import Level

WHITE = (255, 255, 255)

size = (500, 700)
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

level = Level(0.2, 1000, [
            [0.04, 0.9, 0.01, 0.05],  # enemy
            [0.05, 0.4, 0.5, 0.05],  # move
            [0.1, 0.8, 0.001, 0.009],  # stop
            [0.2, 0.8, 0.15, 0.05]  # good
        ], [0.5, 0.5], [0.005, 0.99, 0.005], [0.8, 0.1, 0.1], 'level2')

# Cargar imagen de fondo
background_image = pygame.image.load("resources/images/bg1.png").convert()
background_image = pygame.transform.scale(background_image, size)

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            level.stop()
            sys.exit()

    screen.blit(background_image, (0, 0))  # Dibujar imagen de fondo
    level.draw(screen)

    pygame.display.update()
