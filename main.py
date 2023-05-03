import pygame, sys

from entities.level import Level

WHITE = (255,255,255)
GREEN = (0,255,0)

BLUE = (0,0,255)


size=(500, 700)

screen = pygame.display.set_mode(size)


tecla_a_pulsada = False
tecla_d_pulsada = False

clock = pygame.time.Clock()

level=Level()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            level.stop()
            sys.exit()
    
    clock.tick(10)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] :
        level.movePlayer(-1)
    elif keys[pygame.K_d]:
        level.movePlayer(1)
        
    clock.tick(60)
    screen.fill(WHITE)
    level.draw(screen)
    
    pygame.display.update()