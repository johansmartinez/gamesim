import pygame

from entities.projectile import Projectile

class Player(pygame.sprite.Sprite):
    
    
    def __init__(self, number_lanes, level):
        super().__init__()
        self.level=level
        self.width = 100
        self.height = 70
        self.energy = 100
        self.y_pos= 600
        self.MARGIN = 100
        self.number_lanes= number_lanes
        self.lane= int((number_lanes+1)/2)
        self.x_pos = self.getPixel()
        self.BLACK = (0,0,0)
        self.projectiles=pygame.sprite.Group()
    
    def getProjectiles(self):
        return self.getProjectiles()
    
    def decrease_energy(self, value):
        self.energy-= value
        return self.energy<=0
    
    def validateCollisions(self, projectile):
        self.level.collisions(projectile)
        
    def remove_projectile(self, projectile):
        self.projectiles.remove(projectile)
        
    def shot(self):
        self.projectiles.add(Projectile(self.number_lanes, 0.2,20,self.lane, self))
    
    def move(self, move):
        if ((self.lane +move)>= 1) and ((self.lane + move)<=self.number_lanes):
            self.lane+=move
            self.x_pos= self.getPixel()
        
    def getPixel(self):
        width=500 - self.height - self.MARGIN
        t=width/self.number_lanes
        p= (t*(self.lane-1)) + self.MARGIN 
        return int(p)
        
    def increaseEnergy(self, value):
        if (self.energy+value)<=500:
            self.energy+=value
        else:
            self.energy=500
        
        
    def draw(self, screen):
        rect2 = pygame.Rect(450, (170+(500-self.energy)), 20, self.energy)
        pygame.draw.rect(screen, self.BLACK, rect2)
        rect = pygame.Rect((self.x_pos-(self.width/2)), self.y_pos, self.width, self.height)
        pygame.draw.rect(screen, self.BLACK, rect)
        for p in self.projectiles:
            p.draw(screen)