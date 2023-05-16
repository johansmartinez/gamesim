import pygame
import threading
import time
import numpy as np
import random

from sim.markov import Markov
from sim.montecarlo import montecarlo

from entities.enemy import Enemy

from constants.ViewConstants import ViewConstans
from constants.GameConstants import GameConstants

class Villain(pygame.sprite.Sprite):
    
    def __init__(self, number_lanes, time,life, prob_actions, prob_move,enemy_prob_move, level):
        super().__init__()
        self.level=level
        self.time=time
        self.life = life
        self.total_life = life
        self.y_pos= 40
        self.enemy_prob_move=enemy_prob_move
        self.number_lanes= number_lanes
        self.lane= int((number_lanes+1)/2)
        self.x_pos = self.get_pixel()
        self.prob_move=prob_move
        self.rect= pygame.Rect((self.x_pos-(ViewConstans.WIDTH.value/2)), self.y_pos, ViewConstans.WIDTH.value, ViewConstans.HEIGHT.value)
        self.enemies=pygame.sprite.Group()
        self.actions=Markov(GameConstants.VILLAIN_ACTIONS.value, GameConstants.VILLAIN_INTIAL_ACTION.value, np.array(prob_actions))
        self.thread = threading.Thread(target=self.start)
        self.thread.start()
        
    def get_life(self):
        return self.life
    
    def get_rect(self):
        return self.rect
    
    def move(self, move):
        if ((self.lane +move)>= 1) and ((self.lane + move)<=self.number_lanes):
            self.lane+=move
            self.x_pos= self.get_pixel()
        
    def get_pixel(self):
        width=500 - ViewConstans.HEIGHT.value - ViewConstans.MARGIN.value
        t=width/self.number_lanes
        p= (t*(self.lane-1)) + ViewConstans.MARGIN.value 
        return int(p)
        
    def getEnemies(self):
        return self.enemies
    
    #TODO: cambiar a uno pseudoaletorio
    def select_move(self):
        movimiento= montecarlo(GameConstants.ENEMY_MOVE.value,self.prob_move, random.random())
        self.move(movimiento)
    
    def draw(self, screen):
        rect_life= pygame.Rect(0, 0, int(((self.life*500)/self.total_life)), 20)
        pygame.draw.rect(screen, ViewConstans.VILLAIN_COLOR.value, rect_life)
        self.rect = pygame.Rect((self.x_pos-(ViewConstans.WIDTH.value/2)), self.y_pos, ViewConstans.WIDTH.value, ViewConstans.HEIGHT.value)
        pygame.draw.rect(screen, ViewConstans.VILLAIN_COLOR.value, self.rect)
        for e in self.enemies:
            e.draw(screen)
    
    def decrease_life(self, value):
        self.life-=value
    
    def spawn_enemy(self):
        e=Enemy(self.number_lanes, self.lane, self.enemy_prob_move,self)
        self.enemies.add(e)
    
    def start(self):
        while self.life>0:
            self.actions.next_state()
            actual=self.actions.get_actual_state()
            
            self.do_action(actual)
            
            time.sleep(self.time)
        self.stop()
        
    def do_action(self, state):
        if state=="move":
            self.select_move()
        elif state=="enemy":
            self.spawn_enemy()
        
    def enemy_impact(self, enemy):
        self.level.damage_player(20)
        self.remove_enemy(enemy)
    
    def remove_enemy(self, enemy):
        self.enemies.remove(enemy)
        
    
    def stop(self):
        try:
            self.thread.join()
        except:
            return