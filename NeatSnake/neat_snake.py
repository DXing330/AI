import random

import CONSTANTS as c

class Pos:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def is_collision(self,x,y):
        if (self.x == x and self.y == y):
            return True
        return False

class Fruit:
    def __init__(self,x=0,y=0):
        self.pos = Pos(x,y)

class Snake:
    def __init__(self):
        self.snake = []
        self.fruit = Fruit()
        self.fruit = self.generate_fruit()
        # 0:up, 1:right, 2:down, 3:left
        self.direction = 1
        self.score = 0
        self.eat = False
        self.turn = 0
        self.gameOver = 0
        self.turns = []

    def reset(self):
        self.score = 0
        self.eat = False
        self.turn = 0
        self.turns = []
        self.gameOver = 0
        self.snake = []
        self.snake.append(Pos(int(c.WIDTH/c.BLOCK_SIZE)/2, int(c.HEIGHT/c.BLOCK_SIZE)/2))
        self.snake.append(Pos((int(c.WIDTH/c.BLOCK_SIZE)/2)-1, int(c.HEIGHT/c.BLOCK_SIZE)/2))
        self.snake.append(Pos((int(c.WIDTH/c.BLOCK_SIZE)/2)-2, int(c.HEIGHT/c.BLOCK_SIZE)/2))
        self.direction = 1
        self.fruit = self.generate_fruit()

    def eat_fruit(self):
        self.score += 1
        self.turn = 0
        self.eat = True
        self.fruit = self.generate_fruit()

    def generate_fruit(self):
        fruit_x = random.randint(0, int(c.WIDTH/c.BLOCK_SIZE)-1)
        fruit_y = random.randint(0, int(c.HEIGHT/c.BLOCK_SIZE)-1)
        # Check if the fruit is inside the snake already.
        for i in range(len(self.snake)):
            if (self.snake[i].is_collision(fruit_x,fruit_y)):
                self.generate_fruit()
                break
        return Fruit(fruit_x,fruit_y)
    
    def distance_to_food(self, direction = 0):
        sx = self.snake[0].x
        fx = self.fruit.pos.x
        sy = self.snake[0].y
        fy = self.fruit.pos.y
        if (direction == 0):
            if (sy > fy):
                return sy - fy
        elif (direction == 2):
            if (sy < fy):
                return fy - sy
        elif (direction == 1):
            if (sx < fx):
                return fx - sx
        elif (direction == 3):
            if (sx > fx):
                return sx - fx
        return c.SIZE + 2

    def direction_to_food(self, direction = 0):
        sx = self.snake[0].x
        fx = self.fruit.pos.x
        sy = self.snake[0].y
        fy = self.fruit.pos.y
        if (direction == 0):
            if (sy > fy):
                return 1
        elif (direction == 2):
            if (sy < fy):
                return 1
        elif (direction == 1):
            if (sx < fx):
                return 1
        elif (direction == 3):
            if (sx > fx):
                return 1
        return 0

    def is_collision(self, point = None):
        if (point == None):
            point = self.snake[0]
        for i in range(1, len(self.snake)):
            if (self.snake[i].is_collision(point.x,point.y)):
                return 1
        if (point.x < 0 or point.x >= c.WIDTH/c.BLOCK_SIZE):
            return 2
        if (point.y < 0 or point.y >= c.HEIGHT/c.BLOCK_SIZE):
            return 2
        return 0

    def immediate_danger(self, direction = 0):
        point = Pos(self.snake[0].x, self.snake[0].y)
        if (direction == 0):
            point = Pos(point.x, point.y - 1)
        elif (direction == 2):
            point = Pos(point.x + 1, point.y)
        elif (direction == 4):
            point = Pos(point.x, point.y + 1)
        elif (direction == 6):
            point = Pos(point.x - 1, point.y)
        elif (direction == 1):
            point = Pos(point.x + 1, point.y - 1)
        elif (direction == 3):
            point = Pos(point.x + 1, point.y + 1)
        elif (direction == 5):
            point = Pos(point.x - 1, point.y + 1)
        elif (direction == 7):
            point = Pos(point.x - 1, point.y - 1)
        if (self.is_collision(point)):
            return 1
        return 0

    def distance_to_danger(self, direction = 0):
        distance = 0
        point = Pos(self.snake[0].x, self.snake[0].y)
        if (direction == 0):
            while not (self.is_collision(point)):
                distance += 1
                point = Pos(point.x, point.y - 1)
        elif (direction == 1):
            while not (self.is_collision(point)):
                distance += 1
                point = Pos(point.x + 1, point.y - 1)
        elif (direction == 2):
            while not (self.is_collision(point)):
                distance += 1
                point = Pos(point.x + 1, point.y)
        elif (direction == 3):
            while not (self.is_collision(point)):
                distance += 1
                point = Pos(point.x + 1, point.y + 1)
        elif (direction == 4):
            while not (self.is_collision(point)):
                distance += 1
                point = Pos(point.x, point.y + 1)
        elif (direction == 5):
            while not (self.is_collision(point)):
                distance += 1
                point = Pos(point.x - 1, point.y + 1)
        elif (direction == 6):
            while not (self.is_collision(point)):
                distance += 1
                point = Pos(point.x - 1, point.y)
        elif (direction == 7):
            while not (self.is_collision(point)):
                distance += 1
                point = Pos(point.x - 1, point.y - 1)
        return distance
    
    def move(self):
        self.turn += 1
        # Move the head of the snake first.
        head = self.snake[0]
        if (self.direction == 0):
            new_head = Pos(head.x,(head.y-1))
        elif (self.direction == 1):
            new_head = Pos((head.x+1),(head.y))
        elif (self.direction == 2):
            new_head = Pos((head.x),(head.y+1))
        elif (self.direction == 3):
            new_head = Pos((head.x-1),(head.y))
        self.snake.insert(0, new_head)
        # Then check if the snake has eaten a fruit.
        if (self.fruit.pos.is_collision(new_head.x,new_head.y)):
            # Successfully eaten fruit.
            self.eat_fruit()
        # Failed to eat food.
        else:
            self.snake.pop()
        # Check if the snake has crashed.
        if (self.turn > c.SIZE*(self.score+1)*len(self.snake)):
            self.gameOver = 3
        if (self.gameOver == 0):
            self.gameOver = self.is_collision()

    def vision(self):
        vision = []
        '''for i in range(5):
            vision.append(self.distance_to_danger((2*self.direction+6+i)%8))'''
        for i in range(5):
            vision.append(self.immediate_danger((2*self.direction+6+i)%8))
        '''for i in range(4):
            vision.append(self.distance_to_food(i))'''
        for i in range(4):
            vision.append(self.direction_to_food((self.direction+3+i)%4))
        return vision