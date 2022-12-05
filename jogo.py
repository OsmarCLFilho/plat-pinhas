import pygame
from pygame.locals import *
from loja import Menu

pygame.init()
pygame.mixer.init()

menu = Menu()
menu.menu_principal()
