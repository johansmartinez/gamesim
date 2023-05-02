import pygame
import threading
import time
import numpy as np
import random


class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, number_lanes, time, y_step, lane):
        super().__init__()
        self.time=time
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
        self.hilo = threading.Thread(target=self.start)
        self.hilo.start()
    
    def move(self, move):
        if ((self.lane +move)>= 1) and ((self.lane + move)<=self.number_lanes):
            self.lane+=move
            self.x_pos= self.getPixel()
            
    def move_y(self):
        self.y_pos+=self.y_step
        
    def getPixel(self):
        width=500 - self.height - self.MARGIN
        t=width/self.number_lanes
        p= (t*(self.lane-1)) + self.MARGIN 
        return int(p)
    
    #TODO: cambiar a uno pseudoaletorio
    def select_move(self):
        prob_izquierda = 0.5
        prob_derecha = 0.5
        
        movimiento = random.choices([-1, 1], weights=[prob_izquierda, prob_derecha])[0]
        
        self.move(movimiento)
        
    def draw(self, screen):
        rect = pygame.Rect((self.x_pos-(self.width/2)), self.y_pos, self.width, self.height)
        pygame.draw.rect(screen, self.COLOR, rect)
    
    
    def start(self):
        while self.life>0:
            self.move_y()
            time.sleep(self.time)
        self.stop()
        
    def stop(self):
        self.hilo.join()