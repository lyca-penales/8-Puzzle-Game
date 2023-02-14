import pygame
from pygame.locals import *

#Fonts
pygame.init()
FONT1 = pygame.font.SysFont("cambria", 60)
FONT2 = pygame.font.SysFont("arialblack", 30)
FONT3 = pygame.font.SysFont('calibri', 30)

#Colors (r, g, b)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NAVY = (0, 0, 128)
AQUA = (0, 255, 255)
DODGEERBLUE = (30, 144, 255)
BGCOLOUR = NAVY

#Game Settings/Display Screen
WIDTH = 800
HEIGHT = 630
TITLE = "8 PUZZLE GAME"

#Variables
w = 95
x = 100
y = 100
count = 0
value = 0
solved = False
solving = False
animating = False
s = []
asol = []

#Tile Location
ending_loc = [[x+w*1, y+w*0, 1], [x+w*2, y+w*0, 2], 
        [x+w*0, y+w*1, 3], [x+w*1, y+w*1, 4], [x+w*2, y+w*1, 5], 
        [x+w*0, y+w*2, 6], [x+w*1, y+w*2, 7], [x+w*2, y+w*2, 8]]

starting_loc = [[x+w*0, y+w*0, 3], [x+w*1, y+w*0, 1], [x+w*2, y+w*0, 2],  
        [x+w*0, y+w*1, 7], [x+w*2, y+w*1, 6],
        [x+w*0, y+w*2, 4], [x+w*1, y+w*2, 8], [x+w*2, y+w*2, 5]]

empty_tile = [x+w*1, y+w*1, 0]