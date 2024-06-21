import pygame
pygame.init()

def clamp(x, min = 0, max = 1):
    if (x < min):
        return min
    elif (x > max):
        return max
    return x

S_FONT = 10
L_FONT = 20

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(200,200,200)
GREY = pygame.Color(100,100,100)
RED = pygame.Color(255,0,0)
def shade_red(x):
    return pygame.color(255, int(255*(1-clamp(x))), int(255*(1-clamp(x))))
GREEN = pygame.Color(0,255,0)
BLUE = pygame.Color(0,0,255)

REWARD = 10
BLOCK_SIZE = 60
SIZE = 5
WIDTH = SIZE*BLOCK_SIZE
HEIGHT = SIZE*BLOCK_SIZE