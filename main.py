import pygame, sys

from entities.level import Level

WHITE = (255,255,255)

size=(500, 700)
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

level=Level(0.2, 500, [
            [0.04, 0.9, 0.01, 0.05],  # enemy
            [0.1,  0.9, 0.05, 0.05],  # move
            [0.1, 0.8, 0.001, 0.009],  # stop
            [0.2, 0.8, 0.15, 0.05]   # good
], [0.5, 0.5], [0.01, 0.98, 0.01])
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            level.stop()
            sys.exit()
            
    screen.fill(WHITE)
    level.draw(screen)
    
    pygame.display.update()