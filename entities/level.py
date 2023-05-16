import pygame
from entities.player import Player
from entities.villain import Villain
from constants.GameConstants import GameConstants

class Level(pygame.sprite.Sprite):
    def __init__(self,reaction_villian, villain_life, villain_actions,villain_prob_move, enemy_prob_move):
        super().__init__()
        self.running=True
        self.player=Player(GameConstants.LANES.value, self)
        self.villain=Villain(GameConstants.LANES.value,reaction_villian,villain_life, villain_actions,villain_prob_move,enemy_prob_move, self)
    
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
        collsI = pygame.sprite.spritecollide(projectile, self.villain.getItems(), True)
        for i in collsI:
            #TODO: aplicar efecto
            i.kill()
            projectile.kill()
            
        villian_hit=projectile.get_rect().colliderect(self.villain.get_rect())
        if villian_hit:
            projectile.kill()
            self.player.increaseEnergy(40)
            self.villain.decrease_life(20)
        
    def stop(self):
        self.villain.stop()