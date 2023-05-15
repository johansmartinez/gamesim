import pygame
from entities.player import Player
from entities.villain import Villain

class Level(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.running=True
        self.player=Player(3, self)
        self.villain=Villain(3, 0.2, self)
    
    def damage_player(self, value):
        self.player.decrease_energy(value)
    
    def draw(self,screen):
        self.player.draw(screen)
        self.villain.draw(screen)
        
    def movePlayer(self, move):
        self.player.move(move)
        
    def shot(self):
        self.player.shot()
    
    def collisions(self, projectile):
        colls = pygame.sprite.spritecollide(projectile, self.villain.getEnemies(), True)
        for e in colls:
            self.player.increaseEnergy(20)
            e.kill()
            projectile.kill()
        villian_hit=projectile.get_rect().colliderect(self.villain.get_rect())
        if villian_hit:
            projectile.kill()
            self.villain.decrease_life(20)
        
    def stop(self):
        self.villain.stop()