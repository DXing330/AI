import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('arial', 25)

# Reset
# Reward
# play(action) -> direction
# Game Iteration
# is_collision()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
GREEN = (0, 200, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 60

class SnakeGameAI:
    
    def __init__(self, w=800, h=600):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT
        self.previous_direction = Direction.RIGHT
        self.prev_prev_dir = Direction.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.total_reward = 0
        self.reward = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
    
    def update_reward(self, reward = 1):
        self.reward += reward
        self.total_reward += reward
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def distance_to_food(self, direction):
        if (direction == 0):
            return (self.head.y - self.food.y)/BLOCK_SIZE
        elif (direction == 2):
            return -(self.head.y - self.food.y)/BLOCK_SIZE
        elif (direction == 1):
            return -(self.head.x - self.food.x)/BLOCK_SIZE
        elif (direction == 3):
            return (self.head.x - self.food.x)/BLOCK_SIZE
        
    def play_step(self, action):
        self.reward = 0
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        # Add the new head location to the start of the snake whenever the snake moves.
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self.is_collision() or self.frame_iteration >= 100*len(self.snake):
            game_over = True
            self.reward -= max(10,len(self.snake))
            self.total_reward -= max(10,len(self.snake))
            return self.reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self.reward += max(10,len(self.snake))
            self.total_reward += max(10,len(self.snake))
            self.frame_iteration = 0
            self._place_food()
        # Remove the end of the snake if you move without eating.
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return self.reward, game_over, self.score
    
    def is_collision(self, pt = None):
        if (pt == None):
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        return False

    def distance_to_danger(self, direction = 0):
        pt = Point(self.head.x, self.head.y)
        distance = 0
        if (direction == 0):
            while not (self.is_collision(pt)):
                pt = Point(pt.x, pt.y - BLOCK_SIZE)
                distance += 1
        elif (direction == 1):
            while not (self.is_collision(pt)):
                pt = Point(pt.x + BLOCK_SIZE, pt.y - BLOCK_SIZE)
                distance += 1
        elif (direction == 2):
            while not (self.is_collision(pt)):
                pt = Point(pt.x + BLOCK_SIZE, pt.y)
                distance += 1
        elif (direction == 3):
            while not (self.is_collision(pt)):
                pt = Point(pt.x + BLOCK_SIZE, pt.y + BLOCK_SIZE)
                distance += 1
        elif (direction == 4):
            while not (self.is_collision(pt)):
                pt = Point(pt.x, pt.y + BLOCK_SIZE)
                distance += 1
        elif (direction == 5):
            while not (self.is_collision(pt)):
                pt = Point(pt.x - BLOCK_SIZE, pt.y + BLOCK_SIZE)
                distance += 1
        elif (direction == 6):
            while not (self.is_collision(pt)):
                pt = Point(pt.x - BLOCK_SIZE, pt.y)
                distance += 1
        elif (direction == 7):
            while not (self.is_collision(pt)):
                pt = Point(pt.x - BLOCK_SIZE, pt.y - BLOCK_SIZE)
                distance += 1
        return distance

    def _update_ui(self):
        self.display.fill(BLACK)
        i = 0
        for pt in self.snake:
            if (i == 0):
                i += 1
                pygame.draw.rect(self.display, GREEN, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
                continue
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        text = font.render("Reward: "+ str(self.total_reward), True, WHITE)
        self.display.blit(text, [0, BLOCK_SIZE])
        pygame.display.flip()
        
    def _move(self, action):
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        self.prev_prev_dir = self.previous_direction
        self.previous_direction = self.direction
        pindx = clock_wise.index(self.prev_prev_dir)
        indx = clock_wise.index(self.previous_direction)
        if (action[0] >= 1):
            self.direction = clock_wise[indx] # Continue straight.
        elif (action[1] >= 1):
            self.direction = clock_wise[(indx+1)%len(clock_wise)] # Move right.
            if (pindx == (indx-1)%len(clock_wise)):
                self.update_reward(-1)
        else:
            self.direction = clock_wise[(indx-1+len(clock_wise))%len(clock_wise)] # Move left.
            if (pindx == (indx+1+len(clock_wise))%len(clock_wise)):
                self.update_reward(-1)
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            # Food is right.
            if (self.head.x < self.food.x):
                self.update_reward(1)
            else:
                self.update_reward(-1)
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            # Food is left.
            if (self.head.x > self.food.x):
                self.update_reward(1)
            else:
                self.update_reward(-1)
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            # Food is down.
            if (self.food.y > self.head.y):
                self.update_reward(1)
            else:
                self.update_reward(-1)
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            # Food is up.
            if (self.food.y < self.head.y):
                self.update_reward(1)
            else:
                self.update_reward(-1)
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)