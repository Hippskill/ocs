import numpy.random as random

from core.algorithm import Algorithm
from core.policy import Policy


class Scout(Algorithm):

    def __init__(self, config):
        self.runs_per_instance = config['runs_per_instance']
        self.seed = config['seed']
        self.policy = Policy(config['policy'])

    def choose_best_instance(self, workload, env):
        return None
