import pygame
import threading
import time

from sim.dynamics import mru
from sim.montecarlo import montecarlo

from constants.ViewConstants import ViewConstans
from constants.GameConstants import GameConstants

from utilities.random_number import RandomNumber

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, number_lanes, lane,enemy_prob_move, villain):
        super().__init__()
        self.in_time=0
        self.villain=villain
        self.life = 2
        self.y_pos= 115
        self.enemy_prob_move=enemy_prob_move
        self.number_lanes= number_lanes
        self.lane= lane
        self.x_pos = self.get_pixel()
        self.random= RandomNumber()
        self.rect= pygame.Rect((self.x_pos-(ViewConstans.WIDTH.value/2)), self.y_pos, ViewConstans.WIDTH.value, ViewConstans.HEIGHT.value)
        self.thread = threading.Thread(target=self.start)
        self.thread.start()
    
    def move(self, move):
        if ((self.lane +move)>= 1) and ((self.lane + move)<=self.number_lanes):
            self.lane+=move
            self.x_pos= self.get_pixel()
            
    def move_y(self):
        self.y_pos+=mru(GameConstants.ENEMY_VEL.value, self.in_time)
        if ((self.y_pos+ViewConstans.HEIGHT.value)>=650) :
            self.kill()
            self.villain.enemy_impact(self)
        else:
            self.select_move()
        
    def kill(self):
        self.life=0
        self.villain.remove_enemy(self)
        
    def get_pixel(self):
        width=500 - ViewConstans.HEIGHT.value - ViewConstans.MARGIN.value
        t=width/self.number_lanes
        p= (t*(self.lane-1)) + ViewConstans.MARGIN.value 
        return int(p)
    
    def select_move(self):
        
        movimiento= montecarlo(GameConstants.ENEMY_MOVE.value, self.enemy_prob_move, self.random.calculate_ni())
        self.move(movimiento)
        
    def draw(self, screen):
        self.rect = pygame.Rect((self.x_pos-(ViewConstans.WIDTH.value/2)), self.y_pos, ViewConstans.WIDTH.value, ViewConstans.HEIGHT.value)
        pygame.draw.rect(screen, ViewConstans.ENEMY_COLOR.value, self.rect)
    
    
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