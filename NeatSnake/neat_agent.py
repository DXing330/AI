import random
import neat.population
import neat_snake
import pygame
pygame.init()
clock = pygame.time.Clock()
import os
import neat
import pickle
from CustomCheckpointer import CustomCheckpoint
from node_plots import plot_nodes

pygame.font.init()

import CONSTANTS as c

STAT_FONT = pygame.font.SysFont("comicsans", c.L_FONT)
NODE_FONT = pygame.font.SysFont("comicsans", c.S_FONT)

draw = True

index = 0
generation = 0
max_score = 0
recent_high = [0]
scores = []
avg = 0

win = pygame.display.set_mode((c.WIDTH, c.HEIGHT))

def replay_genome(config_path, winner_filename = "neat_winner.pkl"):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    with open(winner_filename, "rb") as f:
        genome = pickle.load(f)
    genomes = [(1, genome)]
    train(genomes, config, True)

def train(genomes, config, printDetails = False):
    global win, generation, draw, first_person, eight_sided, index, max_score, recent_high, scores, avg, clock
    if printDetails:
        win = pygame.display.set_mode((2*c.WIDTH, c.HEIGHT))

    generation += 1

    tick_speed = 300
    if (printDetails):
        tick_speed = 5
    nets = []
    snakes = []
    ge = []

    o = 0
    for id, genome in genomes:
        o += 1
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(neat_snake.Snake())
        ge.append(genome)
    for i, x in enumerate(snakes):
        x.reset()
        draw = True
    active = True
    while active and len(snakes) > 0:
        clock.tick(tick_speed)

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                active = False
                pygame.quit()
                quit()
        
        for x, snk in enumerate(snakes):
            vision = snakes[x].vision(first_person, eight_sided)
            outputs = nets[x].activate(vision)
            if (printDetails):
                plot_nodes(win, vision, outputs)
            if (first_person):
                for i in range(0,3):
                    if max(outputs) == outputs[i]:
                        if (i == 1):
                            snakes[x].direction = (snakes[x].direction+1)%4
                        elif (i == 2):
                            snakes[x].direction = (snakes[x].direction+3)%4
                        break
            else:
                for i in range(0,4):
                    if max(outputs) == outputs[i]:
                        snakes[x].direction = i
                        break
            snakes[x].move(first_person)

        for x, snk in enumerate(snakes):
            if snk.gameOver > 0:
                ge[x].fitness = snk.fitness()
                scores.append(snk.score)
                recent_high.append(snk.score)
                if (len(recent_high) > 500):
                    recent_high.pop()
                if snk.score > max_score:
                    max_score = snk.score
                nets.pop(x)
                ge.pop(x)
                snakes.pop(x)
            if x < index and draw:
                index = -1
        
        avg = sum(scores)/(len(scores)+1)
        high = max(recent_high)

        try:
            if (snakes[index].gameOver == 0) and draw:
                if not printDetails:
                    win.fill(c.WHITE)
                pygame.draw.rect(win, c.GREEN, pygame.Rect(snakes[index].snake[0].x * c.BLOCK_SIZE, snakes[index].snake[0].y * c.BLOCK_SIZE, c.BLOCK_SIZE, c.BLOCK_SIZE))
                for i in range(1, len(snakes[index].snake)):
                    color = c.BLUE
                    if (i == len(snakes[index].snake) - 1):
                        color = c.GREY
                    pygame.draw.rect(win, color, pygame.Rect(snakes[index].snake[i].x * c.BLOCK_SIZE, snakes[index].snake[i].y * c.BLOCK_SIZE, c.BLOCK_SIZE, c.BLOCK_SIZE))
                pygame.draw.rect(win, c.RED, pygame.Rect(snakes[index].fruit.x * c.BLOCK_SIZE, snakes[index].fruit.y * c.BLOCK_SIZE, c.BLOCK_SIZE, c.BLOCK_SIZE))
                score_label = STAT_FONT.render("Generations: " + str(generation - 1), 1, c.BLACK)
                win.blit(score_label, (10, 10))
                score_label = STAT_FONT.render("Score: " + str(snakes[index].score), 1, c.BLACK)
                win.blit(score_label, (10, 40))
                score_label = STAT_FONT.render("Highscore: " + str(max_score), 1, c.BLACK)
                win.blit(score_label, (10, 70))
                score_label = STAT_FONT.render("Recent: " + str(max_score), 1, c.BLACK)
                win.blit(score_label, (10, 100))
                score_label = STAT_FONT.render("Average: " + str(round(avg, 6)), 1, c.BLACK)
                win.blit(score_label, (10, 130))
                pygame.display.flip()
            else:
                draw = False
        except:
            pass
        pygame.display.flip()

def run(config_file, filename = "fpsavedmodel.pkl", winner_filename = "fpwinner.pkl", new = False):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
    p = neat.Population(config)
    if not new:
        try:
            restore = CustomCheckpoint(filename)
            p = restore.restore_checkpoint(filename)
        except:
            pass
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(CustomCheckpoint(filename))
    winner = p.run(train, 1000)
    with open(winner_filename, "wb") as f:
        pickle.dump(winner, f)
        f.close()

first_person = True
eight_sided = False
local_dir = os.path.dirname(__file__)
if first_person:
    config_path = os.path.join(local_dir, 'config-fp.txt')
else:
    if eight_sided:
        config_path = os.path.join(local_dir, 'config-tp.txt')
    else:
        config_path = os.path.join(local_dir, 'config-tp4.txt')
filenames = ["fpsavedmodel.pkl", "tpsavedmodel.pkl", "tp4savedmodel.pkl"]
winnernames = ["fpwinner.pkl", "tpwinner.pkl", "tp4winner.pkl"]
if first_person:
    filename = filenames[0]
    winnerfile = winnernames[0]
else:
    if eight_sided:
        filename = filenames[1]
        winnerfile = winnernames[1]
    else:
        filename = filenames[2]
        winnerfile = winnernames[2]

run(config_path, filename, winnerfile)
for i in range(10):
    replay_genome(config_path, winnerfile)