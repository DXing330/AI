import torch
import random
import numpy as np
from collections import deque
from snake_game import SnakeGameAI, Direction, Point
from snake_model import Linear_QNet, QTrainer
import helper_plot as helper

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001

class Agent:
    
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY) # remove old memories
        self.model = Linear_QNet(17,400,3)
        self.trainer = QTrainer(self.model, LEARNING_RATE, self.gamma)

    def get_state(self, game):
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN
        state = [
            # Size
            (game.frame_iteration),

            game.distance_to_danger(0),
            game.distance_to_danger(1),
            game.distance_to_danger(2),
            game.distance_to_danger(3),
            game.distance_to_danger(4),
            game.distance_to_danger(5),
            game.distance_to_danger(6),
            game.distance_to_danger(7),

            # Direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.distance_to_food(3),
            game.distance_to_food(1),
            game.distance_to_food(0),
            game.distance_to_food(2)
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
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if (random.randint(1,200) < self.epsilon):
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            # Research torch and tensor and argmax
            state0 = torch.tensor(state,dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        '''state0 = torch.tensor(state,dtype=torch.float)
        prediction = self.model(state0)
        move = torch.argmax(prediction).item()
        final_move[move] = 1'''
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
