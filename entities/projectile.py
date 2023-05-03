import pygame
import threading
import time

class Projectile(pygame.sprite.Sprite):
    
    def __init__(self, number_lanes, time, y_step, lane, player):
        super().__init__()
        self.time=time
        self.player=player
        self.width = 20
        self.height = 20
        self.life = 1
        self.y_pos= 600
        self.y_step= y_step
        self.MARGIN = 100
        self.number_lanes= number_lanes
        self.lane= lane
        self.x_pos = self.getPixel()
        self.COLOR =  (0, 0, 0) 
        self.hilo = threading.Thread(target=self.start)
        self.rect =pygame.Rect((self.x_pos-(self.width/2)), self.y_pos, self.width, self.height)
        self.hilo.start()
    
    def get_rect(self):
        return self.rect
    
    def move(self, move):
        if ((self.lane +move)>= 1) and ((self.lane + move)<=self.number_lanes):
            self.lane+=move
            self.x_pos= self.getPixel()
            
    def move_y(self):
        self.y_pos-=self.y_step
        if (self.y_pos<=38):
            self.kill()
        self.player.validateCollisions(self)
        
    def getPixel(self):
        width=500 - self.height - self.MARGIN
        t=width/self.number_lanes
        p= (t*(self.lane-1)) + self.MARGIN 
        return int(p)
    
    def kill(self):
        self.life=0
        self.player.remove_projectile(self)
        
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
            self.hilo.join()
        except:
            return