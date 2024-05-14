import torch
import random
import numpy as np
from collections import deque
from snake_game import SnakeGameAI, Direction, Point
from snake_model import Linear_QNet, QTrainer
import helper_plot as helper

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.002

class Agent:
    
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY) # remove old memories
        self.model = Linear_QNet(41,600,3)
        self.trainer = QTrainer(self.model, LEARNING_RATE, self.gamma)

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_ll = Point(head.x - 40, head.y)
        point_lll = Point(head.x - 60, head.y)
        point_r = Point(head.x + 20, head.y)
        point_rr = Point(head.x + 40, head.y)
        point_rrr = Point(head.x + 60, head.y)
        point_u = Point(head.x, head.y - 20)
        point_uu = Point(head.x, head.y - 40)
        point_uuu = Point(head.x, head.y - 60)
        point_d = Point(head.x, head.y + 20)
        point_dd = Point(head.x, head.y + 40)
        point_ddd = Point(head.x, head.y + 60)
        point_ur = Point(head.x + 20, head.y - 20)
        point_uur = Point(head.x + 20, head.y - 40)
        point_urr = Point(head.x + 40, head.y - 20)
        point_dr = Point(head.x + 20, head.y + 20)
        point_ddr = Point(head.x + 20, head.y + 40)
        point_drr = Point(head.x + 40, head.y + 20)
        point_dl = Point(head.x - 20, head.y + 20)
        point_ddl = Point(head.x - 20, head.y + 40)
        point_dll = Point(head.x - 40, head.y + 20)
        point_ul = Point(head.x - 20, head.y - 20)
        point_uul = Point(head.x - 20, head.y - 40)
        point_ull = Point(head.x - 40, head.y - 20)
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN
        p_l = game.previous_direction == Direction.LEFT
        p_r = game.previous_direction == Direction.RIGHT
        p_u = game.previous_direction == Direction.UP
        p_d = game.previous_direction == Direction.DOWN
        pp_l = game.prev_prev_dir == Direction.LEFT
        pp_r = game.prev_prev_dir == Direction.RIGHT
        pp_u = game.prev_prev_dir == Direction.UP
        pp_d = game.prev_prev_dir == Direction.DOWN
        state = [
            # Size
            len(game.snake),
            (game.frame_iteration),

            # Danger straight.
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # Danger right.
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            # Danger left.
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # Danger further out.
            game.is_collision(point_rr),
            game.is_collision(point_ll),
            game.is_collision(point_uu),
            game.is_collision(point_dd),
            game.is_collision(point_ur),
            game.is_collision(point_dr),
            game.is_collision(point_dl),
            game.is_collision(point_ul),
            game.is_collision(point_rrr),
            game.is_collision(point_lll),
            game.is_collision(point_uuu),
            game.is_collision(point_ddd),
            game.is_collision(point_uur),
            game.is_collision(point_urr),
            game.is_collision(point_ddr),
            game.is_collision(point_drr),
            game.is_collision(point_ddl),
            game.is_collision(point_dll),
            game.is_collision(point_uul),
            game.is_collision(point_ull),

            # Direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Prev direction
            p_l,
            p_r,
            p_u,
            p_d,

            # Prev Prev direction
            pp_l,
            pp_r,
            pp_u,
            pp_d,

            # Food location
            game.food.x < game.head.x, # food left
            game.food.x > game.head.x, # food right
            game.food.y < game.head.y, # food up
            game.food.y < game.head.y, # food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # List of tuples
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    # This is a very new thing for me.
    def get_action(self, state):
        # random moves: tradeoff exploration/exploitation
        self.epsilon = 40 - self.n_games
        final_move = [0,0,0]
        if (random.randint(1,50) < self.epsilon):
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            # Research torch and tensor and argmax
            state0 = torch.tensor(state,dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record_score = 0
    agent = Agent()
    agent.model.load()
    game = SnakeGameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)
        #get move
        final_move = agent.get_action(state_old)
        # get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if (done):
            # train long memory, plot results
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if (score > record_score):
                record_score = score
                agent.model.save()
            
            #print ("Game: ", agent.n_games, ", Score: ", record_score)
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            #helper.plot(plot_scores, plot_mean_scores)
            #print (plot_scores)
            #print (plot_mean_scores)
            print ("Game: ", agent.n_games, ", Score: ", score, ", Mean: ", mean_score, ", High: ", record_score)


train()
