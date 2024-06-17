import pygame
pygame.init()

import CONSTANTS as c

def plot_nodes(window, inputs, outputs, hidden = []):
    window.fill(c.WHITE)
    size = c.HEIGHT/((len(inputs)*1.5)+2)
    height = size
    for i in range(len(inputs)):
        color = c.BLACK
        if (inputs[i] == 1):
            color = c.RED
        pygame.draw.rect(window, color, pygame.Rect(c.WIDTH+size, height, size, size))
        height += size * 1.5
    size = c.HEIGHT/((len(outputs)*1.5)+2)
    height = size
    for i in range(len(outputs)):
        color = c.BLACK
        if max(outputs) == outputs[i]:
            color = c.RED
        pygame.draw.rect(window, color, pygame.Rect(2*(c.WIDTH-size), height, size, size))
        height += size * 1.5