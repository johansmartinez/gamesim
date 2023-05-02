import pygame, sys
from entities.player import Player
from entities.villain import Villain


WHITE = (255,255,255)
GREEN = (0,255,0)

BLUE = (0,0,255)


size=(500, 700)

screen = pygame.display.set_mode(size)

p=Player(3)
v=Villain(3, 0.2)
tecla_a_pulsada = False
tecla_d_pulsada = False

clock = pygame.time.Clock()

while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            v.stop()
            sys.exit()
    
    clock.tick(10)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] :
        p.move(-1)
    elif keys[pygame.K_d]:
        p.move(1)
        
    clock.tick(60)
    p.increaseEnergy(2)
    screen.fill(WHITE)
    p.draw(screen)
    v.draw(screen)
    
    pygame.display.update()