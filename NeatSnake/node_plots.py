import pygame
pygame.init()

import CONSTANTS as c

def plot_nodes(window, inputs, outputs, hidden = []):
    window.fill(c.WHITE)
    size = c.HEIGHT/((len(inputs)*1.5)+2)
    height = size
    for i in range(len(inputs)):
        color = c.shade_red(inputs[i])
        pygame.draw.rect(window, color, pygame.Rect(c.WIDTH+size, height, size, size))
        height += size * 1.5
    size = c.HEIGHT/((len(outputs)*1.5)+2)
    height = size
    for i in range(len(outputs)):
        color = c.shade_red(outputs[i])
        pygame.draw.rect(window, color, pygame.Rect(2*(c.WIDTH-size), height, size, size))
        height += size * 1.5