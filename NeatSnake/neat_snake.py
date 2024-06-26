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
    
    def pos_collision(self, Pos):
        if (self.x == Pos.x and self.y == Pos.y):
            return True
        return False
    
    def point_in_direction(self, direction, distance = 1):
        x = self.x
        y = self.y
        if (direction == 7 or direction <= 1):
            y -= distance
        elif (3 <= direction <= 5):
            y += distance
        if (1 <= direction <= 3):
            x += distance
        elif (5 <= direction <= 7):
            x -= distance
        return Pos(x,y)
    
    def direction_to_point(self, Pos):
        if (Pos.x == self.x + 1):
            return 1
        elif (Pos.x == self.x - 1):
            return 3
        elif (Pos.y == self.y - 1):
            return 0
        elif (Pos.y == self.y + 1):
            return 2

class Snake:
    def __init__(self):
        self.snake = []
        self.fruit = Pos(-1,-1)
        self.fruit = self.generate_fruit()
        # 0:up, 1:right, 2:down, 3:left
        self.direction = 1
        self.score = 0
        self.turn = 0
        self.gameOver = 0
        self.turns = []

    def reset(self):
        self.score = 0
        self.win = False
        self.turn = 0
        self.total_turns = 0
        self.visited = []
        self.gameOver = 0
        self.snake = []
        self.direction = -1
        self.t_direction = -1
        head = Pos(int(c.SIZE/2)-1, int(c.SIZE/2)-1)
        self.snake.append(head)
        self.snake.append(Pos(int(c.SIZE/2)-2, int(c.SIZE/2)-1))
        self.fruit = self.generate_fruit()

    def visit_tile(self):
        tile_number = self.snake[0].x + (c.SIZE * self.snake[0].y)
        if tile_number in self.visited:
            return
        self.visited.append(tile_number)

    def eat_fruit(self):
        self.score += 1
        self.turn = 0
        self.fruit = self.generate_fruit()

    def generate_fruit(self):
        fruit_x = random.randint(0, int(c.SIZE)-1)
        fruit_y = random.randint(0, int(c.SIZE)-1)
        try:
            # Check if the fruit is inside the snake already.
            for i in range(len(self.snake)):
                if (self.snake[i].is_collision(fruit_x,fruit_y)):
                    return self.generate_fruit()
            return Pos(fruit_x,fruit_y)
        except:
            self.win = True
    
    def distance_to_food(self, direction):
        point = Pos(self.snake[0].x, self.snake[0].y)
        for i in range(c.SIZE+1):
            if (self.fruit.pos_collision(point)):
                return i
            else:
                point = point.point_in_direction(direction)
        return c.SIZE + 1
    
    def distance_to_wall(self, direction):
        point = Pos(self.snake[0].x, self.snake[0].y)
        distance = 0
        while (0 <= point.x < c.SIZE) and (0 <= point.y < c.SIZE):
            point = point.point_in_direction(direction)
            distance += 1
        return distance

    def is_collision(self, point = None):
        if (point == None):
            point = self.snake[0]
        for i in range(1, len(self.snake)):
            if (self.snake[i].is_collision(point.x,point.y)):
                return 1
        if (point.x < 0 or point.x >= c.SIZE):
            return 1
        if (point.y < 0 or point.y >= c.SIZE):
            return 1
        return 0

    def immediate_danger(self, direction):
        point = Pos(self.snake[0].x, self.snake[0].y)
        point = point.point_in_direction(direction)
        if (self.is_collision(point)):
            return 1
        return 0

    def distance_to_danger(self, direction):
        distance = 0
        point = Pos(self.snake[0].x, self.snake[0].y)
        while not (self.is_collision(point)):
            distance += 1
            point = point.point_in_direction(direction)
        return distance
    
    def move(self, fp = True):
        if (self.win):
            self.gameOver = 1
            return
        self.turn += 1
        self.total_turns += 1
        # Move the head of the snake first.
        head = self.snake[0]
        new_head = head.point_in_direction(self.direction*2)
        self.snake.insert(0, new_head)
        if not fp:
            if (self.gameOver == 0):
                self.gameOver = self.is_collision()
                if (self.gameOver > 0):
                    return
        if (self.fruit.is_collision(new_head.x,new_head.y)):
            self.eat_fruit()
            if (self.win):
                self.gameOver = 1
        else:
            self.snake.pop()
        self.t_direction = self.snake[len(self.snake)-1].direction_to_point(self.snake[len(self.snake)-2])
        if (self.gameOver == 0):
            self.gameOver = self.is_collision()
            if (self.gameOver > 0):
                return
        if (self.turn > c.SIZE*c.SIZE+1):
            self.gameOver = 3

    def fp_vision(self):
        vision = []
        food_found = False
        for i in range(5):
            if (self.win):
                vision.append(0)
                vision.append(0)
                vision.append(0)
                continue
            if not food_found:
                food = self.distance_to_food((2*(self.direction)+(i)+6)%8)
                if (food < c.SIZE):
                    food_found = True
                    vision.append(1/food)
                else:
                    vision.append(0)
            else:
                vision.append(0)
            danger = self.distance_to_danger((2*(self.direction)+(i)+6)%8)
            wall = self.distance_to_wall((2*(self.direction)+(i)+6)%8)
            # Body in the way.
            if (danger < wall):
                try:
                    vision.append(1/danger)
                except:
                    vision.append(1)
            else:
                vision.append(0)
            try:
                vision.append(1/wall)
            except:
                vision.append(1)
        return vision
    
    def tp_vision(self, eight = True):
        vision = []
        food_found = False
        for i in range(8):
            if (i%2==1 and not eight):
                continue
            if not food_found:
                food = self.distance_to_food(i)
                if (food < c.SIZE):
                    food_found = True
                    vision.append(1)
                else:
                    vision.append(0)
            else:
                vision.append(0)
            danger = self.distance_to_danger(i)
            wall = self.distance_to_wall(i)
            if (danger < wall):
                vision.append(1)
            else:
                vision.append(0)
            try:
                vision.append(1/wall)
            except:
                vision.append(1)
        # Keep track of you and your tail's direction.
        if (eight):
            for i in range(4):
                if (i == self.direction):
                    vision.append(1)
                else:
                    vision.append(0)
                if (i == self.t_direction):
                    vision.append(1)
                else:
                    vision.append(0)
        return vision

    def vision(self, fp, eight):
        if (fp):
            vision = self.fp_vision()
        else:
            vision = self.tp_vision(eight)
        return vision
    
    def fitness(self):
        fitness = 0
        l = len(self.snake)
        if (self.win):
            fitness += (c.REWARD*c.SIZE*c.SIZE)*c.REWARD*c.REWARD
        fitness += (self.total_turns)
        fitness += (3*(l - 2)*c.REWARD)
        #fitness += ((len(self.visited)**(3/2))*c.REWARD)
        return fitness