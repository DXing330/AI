import random
import neat.population
import neat_snake
import snake as s
import pygame
pygame.init()
clock = pygame.time.Clock()
import os
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-feedforward.txt')
import neat
import pickle
from CustomCheckpointer import CustomCheckpoint

pygame.font.init()

import CONSTANTS as c

STAT_FONT = pygame.font.SysFont("comicsans", 20)

draw = True

index = 0
max_fitness = 0
generation = 0
max_score = 0

win = pygame.display.set_mode((c.WIDTH, c.HEIGHT))

def replay_genome(config_path, winner_filename = "neat_winner.pkl"):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    with open(winner_filename, "rb") as f:
        genome = pickle.load(f)
    genomes = [(1, genome)]
    train(genomes, config, True)

def train(genomes, config, printDetails = False):
    global win, generation, draw, max_fitness, index, max_score, clock

    generation += 1

    tick_speed = 300
    if (printDetails):
        tick_speed = 30
    nets = []
    snakes = []
    ge = []

    max_fitness = 0
    o = 0
    for id, genome in genomes:
        try:
            if genome.fitness > max_fitness:
                max_fitness = genome.fitness
                index = o
        except:
            pass
        o += 1
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        snakes.append(neat_snake.Snake())
        #snakes.append(s.Snake())
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
            snakes[x].move()
            output = nets[x].activate(snakes[x].vision())
            if (printDetails):
                pass
                #print(snakes[x].vision())
                #print(output)
            for  i in range(0,3):
                if max(output) == output[i]:
                    # Punish spinning in circles.
                    snakes[x].turns.append(i)
                    count = len(snakes[x].turns)-1
                    if (count >= 3 and i != 1):
                        if (snakes[x].turns[count] == snakes[x].turns[count-1] and snakes[x].turns[count] == snakes[x].turns[count-2] and snakes[x].turns[count] == snakes[x].turns[count-2]):
                            ge[x].fitness -= 100
                    if i == 0:
                        snakes[x].direction = (snakes[x].direction+1)%4
                        break
                    elif i == 1:
                        break
                    elif i == 2:
                        snakes[x].direction = (snakes[x].direction+3)%4
                        break
                    elif i == 3:
                        change = random.randint(0,2)
                        if (change == 0):
                            snakes[x].direction = (snakes[x].direction+1)%4
                        elif (change == 2):
                            snakes[x].direction = (snakes[x].direction+3)%4
                        break

        for x, snk in enumerate(snakes):
            if snk.gameOver == 0:
                # reward moving towards the food, punish moving away.
                if not (snakes[x].distance_to_food(snakes[x].direction) < c.SIZE):
                    ge[x].fitness -= 1
                if snk.eat:
                    ge[x].fitness += 100
                    snakes[x].eat = False
            elif snk.gameOver > 0:
                # Crash into body.
                if snk.gameOver == 1:
                    ge[x].fitness -= 10
                # Crash into wall.
                elif snk.gameOver == 2:
                    ge[x].fitness -= 100
                # Time Up.
                elif snk.gameOver == 3:
                    ge[x].fitness -= 10
                #draw = False
                if snk.score > max_score:
                    max_score = snk.score
                size = len(snk.snake)
                snk.reset()
                if (size == len(snk.snake)):
                    ge[x].fitness -= 9000
                nets.pop(x)
                ge.pop(x)
                snakes.pop(x)
            if x < index and draw:
                index = -1

        try:
            if (snakes[index].gameOver == 0) and draw:
                win.fill(c.BLACK)
                pygame.draw.rect(win, c.GREEN, pygame.Rect(snakes[index].snake[0].x * c.BLOCK_SIZE, snakes[index].snake[0].y * c.BLOCK_SIZE, c.BLOCK_SIZE, c.BLOCK_SIZE))
                for i in range(1, len(snakes[index].snake)):
                    pygame.draw.rect(win, c.BLUE, pygame.Rect(snakes[index].snake[i].x * c.BLOCK_SIZE, snakes[index].snake[i].y * c.BLOCK_SIZE, c.BLOCK_SIZE, c.BLOCK_SIZE))
                pygame.draw.rect(win, c.RED, pygame.Rect(snakes[index].fruit.pos.x * c.BLOCK_SIZE, snakes[index].fruit.pos.y * c.BLOCK_SIZE, c.BLOCK_SIZE, c.BLOCK_SIZE))
                score_label = STAT_FONT.render("Generations: " + str(generation - 1), 1, (128, 128, 128))
                win.blit(score_label, (10, 10))
                score_label = STAT_FONT.render("Score: " + str(snakes[index].score), 1, (128, 128, 128))
                win.blit(score_label, (10, 40))
                score_label = STAT_FONT.render("Highscore: " + str(max_score), 1, (128, 128, 128))
                win.blit(score_label, (10, 70))
                score_label = STAT_FONT.render("Reward: " + str(ge[index].fitness), 1, (128, 128, 128))
                win.blit(score_label, (10, 100))
                pygame.display.update()
            else:
                draw = False
        except:
            pass
        pygame.display.update()

def run(config_file, new = False, filename = "neatsavedmodel.pkl", winner_filename = "neat_winner.pkl"):
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
    winner = p.run(train, 1)
    with open(winner_filename, "wb") as f:
        pickle.dump(winner, f)
        f.close()

run(config_path)
for i in range(10):
    replay_genome(config_path)