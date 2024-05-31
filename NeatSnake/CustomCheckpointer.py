import gzip
import pickle
import random
import time

from neat.population import Population
from neat.reporting import BaseReporter

class CustomCheckpoint(BaseReporter):

    def __init__(self, filename, generation_interval = 1, time_interval = 60):
        self.filename = filename
        self.generation_interval = generation_interval
        self.time_interval = time_interval

        self.current_gen = None
        self.last_gen_checkpoint = -1
        self.last_time_checkpoint = time.time()

    def start_generation(self, generation):
        self.current_gen = generation

    def end_generation(self, config, population, species_set):
        checkpoint_due = False

        if self.time_interval is not None:
            dt = time.time() - self.last_time_checkpoint
            if dt >= self.time_interval:
                checkpoint_due = True

        if (checkpoint_due is False) and (self.generation_interval is not None):
            dg = self.current_gen - self.last_gen_checkpoint
            if dg >= self.generation_interval:
                checkpoint_due = True

        if checkpoint_due:
            self.save_checkpoint(config, population, species_set,
self.current_gen)
            self.last_gen_checkpoint = self.current_gen
            self.last_time_checkpoint = time.time()

    def save_checkpoint(self, config, population, species_set, generation):
        with gzip.open(self.filename, 'w', compresslevel=5) as f:
            data = (generation, config, population, species_set,
random.getstate())
            pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def restore_checkpoint(filename):
        """Resumes the simulation from a previous saved point."""
        with gzip.open(filename) as f:
            generation, config, population, species_set, rndstate = pickle.load(f)
            random.setstate(rndstate)
            return Population(config, (population, species_set, generation))