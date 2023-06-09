import subprocess
import warnings
import pygame
import sys
import json
import threading
import time
import ctypes
import vlc
import keyboard

from button.Button import Button
from game_controller import GameController


class MenuController():
    def __init__(self):
        pygame.init()
        self.size = (500, 700)
        pygame.display.set_caption("Código maestro")
        self.screen = pygame.display.set_mode(self.size)
        self.gc=None
        self.clock = pygame.time.Clock()
        self.BG = pygame.image.load("resources/assets/backmenu.png")
        
        #video = mp.VideoFileClip("resources/kinematics/prologo.mp4")
        #audio = mp.AudioFileClip("resources/kinematics/prologo.mp4")
        #audio = audio.fx(mp.vfx.speedx, factor=0.46)
        #video = video.set_audio(audio)
        #video.preview()
        
        #warnings.filterwarnings("ignore", category=UserWarning, module=".*libpng.*")
        
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new("resources/kinematics/prologo.mp4")
        player.set_media(media)
        player.set_fullscreen(True)
        player.play()
        
        def close_video():
            player.stop()
            
        keyboard.on_press_key("space", lambda _: close_video())
        
        while player.get_state() != vlc.State.Stopped:
            pass
        
        self.main_menu()
        
    def read_level(self):
        path = "resources/config/level.json"
        with open(path, "r") as file:
            return json.load( file)

    def get_font(self, size): # Returns Press-Start-2P in the desired size
        return pygame.font.Font("resources/assets/font.ttf", size)
    
    def end(self):
        print("----------------me mandaron a cerrar el juego--------------------")
        self.close()

    def restart(self):
        pygame.mixer.init()
        self.gc=None
        r_flag=True
        ve_sound = pygame.mixer.Sound("resources/music/lose.wav")
        pygame.mixer.Sound.play(ve_sound)
        while r_flag:
            self.screen.fill('black')
            IM = pygame.image.load("resources/assets/gameover.png")
            self.screen.blit(IM, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    r_flag=False
                    self.close()
            
            pygame.display.update()
            time.sleep(3)
            r_flag=False
        
        for t in threading.enumerate():
            try:
                if t.getName()!='MainThread':
                    thread_id = t.ident
                    thread_object = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))
                    if thread_object == 0:
                        raise ValueError("El hilo no pudo ser detenido")
            except Exception as e:
                print(str(e))
        
        self.close()
        
    def close(self):
        try:
            pygame.display.quit()
            pygame.mixer.quit()
            pygame.quit()
            sys.exit()
        except Exception as e:
            print(str(e))
            
    def instructions(self):
        i_flag=True
        while i_flag:
            self.screen.fill('black')
            IM = pygame.image.load("resources/assets/inst.png")
            self.screen.blit(IM, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()


            QUIT_BUTTON = Button(image=None, pos=(250, 600), 
                                text_input="Regresar", font=self.get_font(25), base_color="#d7fcd4", hovering_color="orange")


            for button in [QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        i_flag=False
                        self.main_menu()

            pygame.display.flip()
            
    def play(self):
        N_L=self.read_level()['level']
        self.gc=GameController(self.screen,N_L, self)

    def main_menu(self):
        mm_flag=True
        while mm_flag:
            self.screen.fill('black')
            self.screen.blit(self.BG, (0, 0))

            MENU_MOUSE_POS = pygame.mouse.get_pos()


            PLAY_BUTTON = Button(image=None, pos=(100, 500), 
                                text_input="Jugar", font=self.get_font(25), base_color="#d7fcd4", hovering_color="orange")
            INSTR_BUTTON = Button(image=None, pos=(200, 550), 
                                text_input="Instrucciones", font=self.get_font(25), base_color="#d7fcd4", hovering_color="orange")
            QUIT_BUTTON = Button(image=None, pos=(100, 600), 
                                text_input="Salir", font=self.get_font(25), base_color="#d7fcd4", hovering_color="orange")


            for button in [PLAY_BUTTON, INSTR_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        mm_flag=False
                        self.play()
                    if INSTR_BUTTON.checkForInput(MENU_MOUSE_POS):
                        mm_flag=False
                        self.instructions()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        mm_flag=False
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
