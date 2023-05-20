import pygame
import threading

from entities.projectile import Projectile

from constants.ViewConstants import ViewConstans
from constants.GameConstants import GameConstants

class Player(pygame.sprite.Sprite):
    
    
    def __init__(self, number_lanes, level):
        super().__init__()
        self.level=level
        self.running=True
        self.energy = GameConstants.INITIAL_ENERGY.value
        self.y_pos= 600
        self.number_lanes= number_lanes
        self.lane= int((number_lanes+1)/2)
        self.x_pos = self.get_pixel()
        self.projectiles=pygame.sprite.Group()
        self.thread = threading.Thread(target=self.start)
        self.thread.start()
        
        # Cargar imagen del personaje
        self.image = pygame.image.load("resources/images/player/player.png").convert_alpha()
        # Ajustar tamaño de la imagen si es necesario
        # self.image = pygame.transform.scale(self.image, (ancho, alto))
        # Obtener rectángulo del área ocupada por la imagen
        self.rect = self.image.get_rect()
        # Asignar posición del rectángulo
        self.rect.center = (self.x_pos, self.y_pos)
        pygame.mixer.init()
    
    def getProjectiles(self):
        return self.projectiles
    
    def decrease_energy(self, value):
        self.energy-= value
        return self.energy<=0
    
    def validateCollisions(self, projectile):
        self.level.collisions(projectile)
        
    def remove_projectile(self, projectile):
        self.projectiles.remove(projectile)
        
    def shot(self):
        shot_sound = pygame.mixer.Sound("resources/music/shot.wav")
        pygame.mixer.Sound.play(shot_sound)
        self.projectiles.add(Projectile(self.number_lanes,self.lane, self))
    
    def ultimate_villain(self):
        if self.energy==GameConstants.MAX_ENERGY.value:
            shot_sound = pygame.mixer.Sound("resources/music/ultimate.wav")
            pygame.mixer.Sound.play(shot_sound)
            self.level.ultimate_villain()
            self.energy=GameConstants.INITIAL_ENERGY.value
    
    def move(self, move):
        if ((self.lane + move) >= 1) and ((self.lane + move) <= self.number_lanes):
            self.lane += move
            self.x_pos = self.get_pixel()
            # Actualizar la posición del rectángulo con las nuevas coordenadas
            self.rect.center = (self.x_pos, self.y_pos)
        
    def get_pixel(self):
        width=500 - ViewConstans.HEIGHT.value - ViewConstans.MARGIN.value
        t=width/self.number_lanes
        p= (t*(self.lane-1)) + ViewConstans.MARGIN.value 
        return int(p)
        
    def increaseEnergy(self, value):
        if (self.energy+value)<=GameConstants.MAX_ENERGY.value:
            self.energy+=value
        else:
            self.energy=GameConstants.MAX_ENERGY.value
        
    def draw(self, screen):
        rect2 = pygame.Rect(450, (170+(GameConstants.MAX_ENERGY.value-self.energy)), 20, self.energy)
        pygame.draw.rect(screen, ViewConstans.PLAYER_COLOR.value, rect2)
        screen.blit(self.image, self.rect)
        for p in self.projectiles:
            p.draw(screen)
            
    def start(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(12)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a] :
                self.move(-1)
            elif keys[pygame.K_d]:
                self.move(1)
            elif keys[pygame.K_k]:
                self.shot()
            elif keys[pygame.K_l]:
                self.ultimate_villain()
        
        self.stop()
        
    def stop(self):
        try:
            self.running=False
            self.thread.join()
        except:
            return