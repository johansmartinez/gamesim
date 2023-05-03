import pygame
from entities.player import Player
from entities.villain import Villain

class Level(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player=Player(3)
        self.villain=Villain(3, 0.2, self)
    
    def damage_player(self, value):
        self.player.decrease_energy(value)
    
    def draw(self,screen):
        self.player.draw(screen)
        self.villain.draw(screen)
        
    def movePlayer(self, move):
        self.player.move(move)
        
    def stop(self):
        self.villain.stop()