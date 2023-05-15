import pygame
import threading
import time
import numpy as np
import random
from utilities import num


class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, number_lanes, time, y_step, lane, villain):
        super().__init__()
        self.time=time
        self.villain=villain
        self.width = 100
        self.height = 70
        self.life = 2
        self.y_pos= 115
        self.y_step= y_step
        self.MARGIN = 100
        self.number_lanes= number_lanes
        self.lane= lane
        self.x_pos = self.getPixel()
        self.COLOR =  (255, 87, 51) 
        self.rect= pygame.Rect((self.x_pos-(self.width/2)), self.y_pos, self.width, self.height)
        self.hilo = threading.Thread(target=self.start)
        self.hilo.start()
    
    def move(self, move):
        if ((self.lane +move)>= 1) and ((self.lane + move)<=self.number_lanes):
            self.lane+=move
            self.x_pos= self.getPixel()
            
    def move_y(self):
        self.y_pos+=self.y_step
        if ((self.y_pos+self.height)>=650) :
            self.kill()
            self.villain.enemy_impact(self)
        else:
            self.select_move()
        
    def kill(self):
        self.life=0
        self.villain.remove_enemy(self)
        
    def getPixel(self):
        width=500 - self.height - self.MARGIN
        t=width/self.number_lanes
        p= (t*(self.lane-1)) + self.MARGIN 
        return int(p)
    
    #TODO: cambiar a uno pseudoaletorio
    def select_move(self):
        #movimiento = random.choices([-1,0, 1], weights=[0.1,0.8, 0.1])[0]
        movimiento=num.move_model()
        self.move(movimiento)
        
    def draw(self, screen):
        self.rect = pygame.Rect((self.x_pos-(self.width/2)), self.y_pos, self.width, self.height)
        pygame.draw.rect(screen, self.COLOR, self.rect)
    
    
    def start(self):
        while self.life>0:
            self.move_y()
            time.sleep(self.time)
        self.stop()
        
    def stop(self):
        try:
            self.kill()
            self.hilo.join()
        except:
            return