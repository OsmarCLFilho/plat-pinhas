import pygame as pg
import numpy as np
import dev_game as gs #game_src
import menu as mn

PLAYER_SPEED = 10
CAMERA_DISTANCE = 15
GRAVITY = 40
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 700
MOUSE_SENSITIVITY = 0.1

pg.display.init()
pg.mixer.init()
pg.font.init()

surface = pg.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))

def start_game():
    print("starting")

start_button = mn.Btn("Start", start_game, color=(46,52,64))

def exit_all():
    print("exiting")

exit_button = mn.Btn("Exit", exit_all, color=(46,52,64))

def start_market():
    print("it's upgrading time")

shop_button = mn.Btn("Upgrades", start_market, color=(46,52,64))

menu = mn.Menu(surface=surface,
               btns=(start_button, exit_button, shop_button),
               cx=SCREEN_WIDTH/2, cy=SCREEN_HEIGHT/2,
               darkc=(100,100,100), lightc=(170,170,170))

game = gs.Game(surface=surface, player_speed=PLAYER_SPEED, camera_distance=CAMERA_DISTANCE, gravity=GRAVITY, mouse_sensitivity=MOUSE_SENSITIVITY)

#pg.mixer.music.load('song.mp3')
#pg.mixer.music.set_volume(0.2)
#pg.mixer.music.play()

menu.start()

game.start_game()

pg.display.quit()
pg.mixer.quit()
pg.font.quit()
