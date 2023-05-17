import pygame

from entities.player import Player
from entities.villain import Villain
from constants.GameConstants import GameConstants

class Level(pygame.sprite.Sprite):
    def __init__(self,reaction_villian, villain_life, villain_actions,villain_prob_move, enemy_prob_move, prob_items):
        super().__init__()
        self.running=True
        self.double_damage=False
        self.frezee_flag=False
        self.hit_count=0
        self.max_hits=0
        self.player=Player(GameConstants.LANES.value, self)
        self.villain=Villain(GameConstants.LANES.value,reaction_villian,villain_life, villain_actions,villain_prob_move,enemy_prob_move,prob_items, self)
    
    def get_frezee_flag(self):
        return self.frezee_flag
    
    def set_frezee_flag(self, value):
        self.frezee_flag=value
    
    def damage_player(self, value):
        dead=self.player.decrease_energy(value)
        if dead:
            self.stop()
    
    def ultimate_villain(self):
        dead=self.villain.ultimate_villain()
        if dead:
            self.stop()
    
    def draw(self,screen):
        self.player.draw(screen)
        self.villain.draw(screen)
    
    def collisions(self, projectile):
        colls = pygame.sprite.spritecollide(projectile, self.villain.getEnemies(), True)
        for e in colls:
            self.player.increaseEnergy(20)
            e.kill()
            projectile.kill()
        collsI = pygame.sprite.spritecollide(projectile, self.villain.getItems(), True)
        for i in collsI:
            self.powerup(i.get_power())
            i.kill()
            projectile.kill()
            
        villian_hit=projectile.get_rect().colliderect(self.villain.get_rect())
        if villian_hit:
            projectile.kill()
            self.player.increaseEnergy(40)
            
            dead=self.villain.decrease_life(self.calculate_damage(GameConstants.DAMAGE_SHOT.value))
            if dead:
                self.stop()
        
    def calculate_damage(self, damage):
        if self.double_damage:
            if self.hit_count<=self.max_hits:
                self.hit_count+=1
                return damage*2
            else:
                self.double_damage=False
                self.hit_count=0
                self.max_hits=0
                return damage
        else:
            return damage
            
    def double_power(self):
        self.double_damage=True
        self.max_hits+=GameConstants.HITS_COUNT.value
        
    def powerup(self, power):
        if power=="frezee":
            self.frezee()
        elif power=="double":
            self.double_power()
        elif power=="energy":
            self.player.increaseEnergy(20)
    
    def frezee(self):
        self.frezee_flag=True
        
    def stop(self):
        self.villain.stop()
        self.player.stop()