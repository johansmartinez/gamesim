import pygame
import threading
import time
import numpy as np

from sim.markov import Markov
from sim.montecarlo import montecarlo

from entities.enemy import Enemy
from entities.item import Item

from constants.ViewConstants import ViewConstans
from constants.GameConstants import GameConstants
from utilities.random_number import RandomNumber

class Villain(pygame.sprite.Sprite):
    
    def __init__(self, number_lanes, time,life, prob_actions, prob_move,enemy_prob_move, prob_items ,path_level,level):
        super().__init__()
        self.level=level
        self.path_level=path_level
        self.time=time
        self.life = life
        self.total_life = life
        self.ultimate=False
        self.random= RandomNumber()
        self.y_pos= 40
        self.frezee_count=0
        self.enemy_prob_move=enemy_prob_move
        self.prob_items=prob_items
        self.number_lanes= number_lanes
        self.lane= int((number_lanes+1)/2)
        self.x_pos = self.get_pixel()
        self.prob_move=prob_move
        self.rect= pygame.Rect((self.x_pos-(ViewConstans.WIDTH.value/2)), self.y_pos, ViewConstans.WIDTH.value, ViewConstans.HEIGHT.value)
        self.enemies=pygame.sprite.Group()
        self.items=pygame.sprite.Group()
        self.actions=Markov(GameConstants.VILLAIN_ACTIONS.value, GameConstants.VILLAIN_INTIAL_ACTION.value, np.array(prob_actions))
        self.thread = threading.Thread(target=self.start)
        self.thread.start()
        
        # Cargar imagen del villano
        self.get_boss_image()
        # Ajustar tamaño de la imagen si es necesario
        # self.image = pygame.transform.scale(self.image, (ancho, alto))
        # Obtener rectángulo del área ocupada por la imagen
        
        
    def get_life(self):
        return self.life
    
    def get_rect(self):
        return self.rect
    
    def move(self, move):
        if ((self.lane + move) >= 1) and ((self.lane + move) <= self.number_lanes):
            self.lane += move
            self.x_pos = self.get_pixel()
            self.rect.center = (self.x_pos, self.y_pos+30)  # Actualizar la posición del rectángulo

    def set_ultimate(self, value):
        self.ultimate=value
        
    def get_pixel(self):
        width = 500 - ViewConstans.HEIGHT.value - ViewConstans.MARGIN.value
        t = width / self.number_lanes
        p = (t * (self.lane - 1)) + ViewConstans.MARGIN.value
        return int(p)
        
    def getEnemies(self):
        return self.enemies
    
    def getItems(self):
        return self.items
    
    def select_move(self):
        movimiento= montecarlo(GameConstants.VILLAIN_MOVE.value,self.prob_move, self.random.calculate_ni())
        self.move(movimiento)
    
    def get_boss_image(self):
        path="resources/images/"
        if self.level.get_frezee_flag():
            path+=f"{self.path_level}/boss_frezee.png"
        else:
            path+=f"{self.path_level}/boss.png"
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x_pos, self.y_pos+30)
    
    def draw(self, screen):
        self.get_boss_image()
        rect_life= pygame.Rect(0, 0, int(((self.life*500)/self.total_life)), 20)
        pygame.draw.rect(screen, ViewConstans.VILLAIN_COLOR.value, rect_life)
        screen.blit(self.image, self.rect)  # Dibujar la imagen en lugar del rectángulo
        if self.ultimate:
            rect_ultimate=pygame.Rect(self.get_pixel(), 45, 70,71)
            ult_image = pygame.image.load("resources/images/player/ult.png").convert_alpha()
            screen.blit(ult_image, rect_ultimate)
        for e in self.enemies:
            e.draw(screen)
        for i in self.items:
            i.draw(screen)
    
    def decrease_life(self, value):
        self.life-=value
        return self.life<=0
    
    def ultimate_villain(self):
        self.ultimate=True
        self.life-=self.total_life/25
        return self.life<=0
    
    def spawn_enemy(self):
        e=Enemy(self.number_lanes, self.lane, self.enemy_prob_move,self)
        self.enemies.add(e)
        
    def spawn_items(self):
        power=montecarlo(GameConstants.ITEMS_POWERS.value, self.prob_items, self.random.calculate_ni())
        i=Item(self.number_lanes, self.lane,power,self)
        self.items.add(i)
        
    def frezee(self):
        self.frezee_count+=1
        if self.frezee_count>=GameConstants.FREEZE_COUNT_FLAG.value:
            self.frezee_count=0
            self.level.set_frezee_flag(False)
    
    def start(self):
        while self.life > 0:
            if self.ultimate:
                self.ultimate=False
            if self.level.get_frezee_flag():
                self.frezee()
            else:
                self.actions.next_state()
                actual = self.actions.get_actual_state()

                self.do_action(actual)

            time.sleep(self.time)
        self.stop()
        
    def do_action(self, state):
        if state=="move":
            self.select_move()
        elif state=="enemy":
            self.spawn_enemy()
        elif state=="good":
            self.spawn_items()
        
    def enemy_impact(self, enemy):
        self.level.damage_player(20)
        self.remove_enemy(enemy)
    
    def remove_enemy(self, enemy):
        self.enemies.remove(enemy)
    
    def remove_item(self, item):
        self.items.remove(item)
        
    
    def stop(self):
        try:
            self.thread.join()
        except:
            return