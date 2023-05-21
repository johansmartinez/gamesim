import pygame


from entities.level import Level

WHITE = (255, 255, 255)

size = (500, 700)
screen = pygame.display.set_mode(size)



level = Level(0.2, 2000, [
            [0.04, 0.9, 0.01, 0.05],  # enemy
            [0.05, 0.4, 0.5, 0.05],  # move
            [0.1, 0.8, 0.001, 0.009],  # stop
            [0.2, 0.8, 0.15, 0.05]  # good
        ], [0.5, 0.5], [0.005, 0.99, 0.005], [0.3, 0.3, 0.4], 'level2')

# Cargar imagen de fondo

while True:
    

    
    level.draw(screen)

    pygame.display.update()
