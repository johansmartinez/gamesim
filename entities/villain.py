import pygame
import threading
import time
import numpy as np
import random

from sim.markov import Markov
from entities.enemy import Enemy

class Villain(pygame.sprite.Sprite):
    
    def __init__(self, number_lanes, time):
        super().__init__()
        self.time=time
        self.width = 100
        self.height = 70
        self.life = 100
        self.y_pos= 40
        self.MARGIN = 100
        self.number_lanes= number_lanes
        self.lane= int((number_lanes+1)/2)
        self.x_pos = self.getPixel()
        self.RED = (255,0,0)
        self.enemies=[]
        self.actions=Markov(["enemy", "move", "stop", "good"], "stop", np.array([
            [0.01, 0.9, 0.07, 0.02],  # enemy
            [0.3,  0.6, 0.05, 0.05],  # move
            [0.2, 0.6, 0.01, 0.19],  # stop
            [0.2, 0.7, 0.05, 0.05]   # good
        ]))
        self.hilo = threading.Thread(target=self.start)
        self.hilo.start()
    
    def move(self, move):
        if ((self.lane +move)>= 1) and ((self.lane + move)<=self.number_lanes):
            self.lane+=move
            self.x_pos= self.getPixel()
        
    def getPixel(self):
        width=500 - self.height - self.MARGIN
        t=width/self.number_lanes
        p= (t*(self.lane-1)) + self.MARGIN 
        return int(p)
        
    
    #TODO: cambiar a uno pseudoaletorio
    def select_move(self):
        # Definir las probabilidades de moverse a la izquierda o a la derecha
        prob_izquierda = 0.5
        prob_derecha = 0.5
        
        # Generar un número aleatorio para decidir si moverse a la izquierda o a la derecha
        movimiento = random.choices([-1, 1], weights=[prob_izquierda, prob_derecha])[0]
        
        # Hacer algo con el movimiento (por ejemplo, actualizar la posición del villano)
        self.move(movimiento)
        
    def draw(self, screen):
        rect = pygame.Rect((self.x_pos-(self.width/2)), self.y_pos, self.width, self.height)
        pygame.draw.rect(screen, self.RED, rect)
        for e in self.enemies:
            e.draw(screen)
    
    def spawn_enemy(self):
        e=Enemy(self.number_lanes, self.time, 20, self.lane)
        self.enemies.append(e)
    
    def start(self):
        while self.life>0:
            # Actualizar el estado del villano
            self.actions.next_state()
            actual=self.actions.get_actual_state()
            
            # Hacer algo con el estado (por ejemplo, imprimirlo en pantalla)
            print("Villano está", actual)
            self.do_action(actual)
            
            #TODO: elimianr línea 
            self.life= self.life-1
            
            # Esperar un tiempo antes de actualizar el estado de nuevo
            time.sleep(self.time)
        self.stop()
        
    def do_action(self, state):
        if state=="move":
            self.select_move()
        elif state=="enemy":
            self.spawn_enemy()
        
        
    def stop(self):
        print("deteniendo")
        self.hilo.join()