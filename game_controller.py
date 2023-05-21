import pygame
import sys
from button.Button import Button

from entities.level import Level 
from constants.GameConstants import GameConstants

class GameController():
    def __init__(self, screen, menus):
        self.number_level=1
        self.actual_level=None
        self.screen=screen
        self.menus=menus
        self.running_level=False
        self.screen.fill('black')
        pygame.display.update()
        self.init()
        
    def get_font(self, size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("resources/assets/font.ttf", size)
    
        
    def init(self):
        self.get_level_instance()
        clock = pygame.time.Clock()
        self.running_level=True
        while self.running_level:
            print("init")
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_level=False
                    self.actual_level.stop()
                    sys.exit()
            if self.actual_level!=None:
                self.actual_level.draw(self.screen)
            
            pygame.display.update()
            
    def finish_level(self):
        self.running_level=False
        self.actual_level=None
        self.menus.restart()
    
    def next_level(self):
        if (self.number_level+1)>GameConstants.MAX_LEVELS.value:
            print('finalizó todo')
            #TODO: videó final
        else:
            self.number_level=self.number_level+1
            self.get_level_instance()
            
    def get_level_instance(self):
        if self.number_level==1:
            self.actual_level = Level(self,0.2, 10, [
            [0.04, 0.9, 0.01, 0.05],  # enemy
            [0.05, 0.4, 0.5, 0.05],  # move
            [0.1, 0.8, 0.001, 0.009],  # stop
            [0.2, 0.8, 0.15, 0.05]  # good
            ], [0.5, 0.5], [0.005, 0.99, 0.005], [0.3, 0.3, 0.4], 'level1')
        elif self.number_level==2:
            self.actual_level = Level(self,0.2, 10, [
            [0.04, 0.9, 0.01, 0.05],  # enemy
            [0.05, 0.4, 0.5, 0.05],  # move
            [0.1, 0.8, 0.001, 0.009],  # stop
            [0.2, 0.8, 0.15, 0.05]  # good
            ], [0.5, 0.5], [0.005, 0.99, 0.005], [0.3, 0.3, 0.4], 'level2')
        elif self.number_level==3:
            self.actual_level = Level(self,0.2, 10, [
            [0.04, 0.9, 0.01, 0.05],  # enemy
            [0.05, 0.4, 0.5, 0.05],  # move
            [0.1, 0.8, 0.001, 0.009],  # stop
            [0.2, 0.8, 0.15, 0.05]  # good
            ], [0.5, 0.5], [0.005, 0.99, 0.005], [0.3, 0.3, 0.4], 'level3')
        elif self.number_level==4:
            self.actual_level = Level(self,0.2, 10, [
            [0.04, 0.9, 0.01, 0.05],  # enemy
            [0.05, 0.4, 0.5, 0.05],  # move
            [0.1, 0.8, 0.001, 0.009],  # stop
            [0.2, 0.8, 0.15, 0.05]  # good
            ], [0.5, 0.5], [0.005, 0.99, 0.005], [0.3, 0.3, 0.4], 'level4')
        else:
            self.actual_level = Level(self,0.2, 10, [
            [0.04, 0.9, 0.01, 0.05],  # enemy
            [0.05, 0.4, 0.5, 0.05],  # move
            [0.1, 0.8, 0.001, 0.009],  # stop
            [0.2, 0.8, 0.15, 0.05]  # good
            ], [0.5, 0.5], [0.005, 0.99, 0.005], [0.3, 0.3, 0.4], 'level5')