import pygame
import threading
import time
import numpy as np
import random

from sim.dynamics import free_fall
from sim.montecarlo import montecarlo

from constants.ViewConstants import ViewConstans
from constants.GameConstants import GameConstants

class Item(pygame.sprite.Sprite):
    
    def __init__(self, number_lanes, lane, villain):
        super().__init__()
        self.in_time=0
        self.villain=villain
        self.life = 2
        self.y_pos= 115
        self.number_lanes= number_lanes
        self.lane= lane
        self.x_pos = self.get_pixel()
        self.rect= pygame.Rect((self.x_pos-(ViewConstans.WIDTH.value/2)), self.y_pos, ViewConstans.WIDTH.value, ViewConstans.HEIGHT.value)
        self.thread = threading.Thread(target=self.start)
        self.thread.start()
    
    def move_y(self):
        self.y_pos+=free_fall(GameConstants.ITEM_GRAVITY.value, self.in_time)
        if ((self.y_pos+ViewConstans.HEIGHT.value)>=650) :
            self.kill()
        
    def kill(self):
        self.life=0
        self.villain.remove_item(self)
        
    def get_pixel(self):
        width=500 - ViewConstans.HEIGHT.value - ViewConstans.MARGIN.value
        t=width/self.number_lanes
        p= (t*(self.lane-1)) + ViewConstans.MARGIN.value 
        return int(p)
    
    #TODO: cambiar a uno pseudoaletorio
    def select_move(self):
        
        movimiento= montecarlo(GameConstants.ENEMY_MOVE.value, self.enemy_prob_move, random.random())
        self.move(movimiento)
        
    def draw(self, screen):
        self.rect = pygame.Rect((self.x_pos-(ViewConstans.WIDTH.value/2)), self.y_pos, ViewConstans.WIDTH.value, ViewConstans.HEIGHT.value)
        pygame.draw.rect(screen, ViewConstans.ITEM_COLOR.value, self.rect)
    
    
    def start(self):
        while self.life>0:
            self.in_time+=GameConstants.OBJ_THREAD_TIME.value
            self.move_y()
            time.sleep(GameConstants.OBJ_THREAD_TIME.value)
        self.stop()
        
    def stop(self):
        try:
            self.kill()
            self.thread.join()
        except:
            return