import pygame, sys

from entities.level import Level

WHITE = (255,255,255)

size=(500, 700)

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

level=Level(0.2,500, [
            [0.01, 0.9, 0.07, 0.02],  # enemy
            [0.2,  0.7, 0.05, 0.05],  # move
            [0.2, 0.6, 0.01, 0.19],  # stop
            [0.2, 0.7, 0.05, 0.05]   # good
], [0.5, 0.5], [0.01, 0.98, 0.01])
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            level.stop()
            sys.exit()
    
    clock.tick(12)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] :
        level.movePlayer(-1)
    elif keys[pygame.K_d]:
        level.movePlayer(1)
    elif keys[pygame.K_k]:
        level.shot()
        
    clock.tick(60)
    screen.fill(WHITE)
    level.draw(screen)
    
    pygame.display.update()