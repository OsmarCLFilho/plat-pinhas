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

surface = pg.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
game = gs.Game(surface=surface, player_speed=PLAYER_SPEED, camera_distance=CAMERA_DISTANCE, gravity=GRAVITY, mouse_sensitivity=MOUSE_SENSITIVITY)

#pg.mixer.music.load('song.mp3')
#pg.mixer.music.set_volume(0.2)
#pg.mixer.music.play()

#game loop
game.start_game()

pg.display.quit()
#pg.mixer.quit()
