import numpy.random as random

from core.algorithm import Algorithm
from core.policy import Policy


class Scout(Algorithm):

    def __init__(self, config):
        self.runs_per_instance = config['runs_per_instance']
        self.seed = config['seed']
        self.policy = Policy(config['policy'])
        self.probability_threshold = config['probability_threshold']
        self.iters = config['iters']

    def choose_best_instance(self, workload, env):
        random.seed(self.seed)

        avaliable_instances = env.get_avaliable_instances()

        random.shuffle(avaliable_instances)

        best_instance = avaliable_instances[0]
        print('start scout from', best_instance)

        for _ in range(self.iters):
            suitable_instances = self.find_suitable_instances(best_instance, workload, env)
            best_instance = self.select_best_instance(suitable_instances, workload, env)

        return  best_instance

    def find_suitable_instances(self, best_instance, workload, env):
        suitable_instances = [best_instance]

        avaliable_instances = env.get_avaliable_instances()

        for instance in avaliable_instances:
            probability = self.estimate_probability(best_instance, instance)

            if probability > self.probability_threshold:
                print('add candidate', instance, 'with probability', probability)
                suitable_instances.append(instance)

        return suitable_instances

    # returns probability that candidate instance will be better than best instance
    def estimate_probability(self, best_instance, candidate):
        # TODO(nmikhaylov): implement compare
        # ¯\_(ツ)_/¯
        return random.random()

    def select_best_instance(self, suitable_instances, workload, env):
        instances_with_run_results = []

        for suitable_instance in suitable_instances:
            print('try', suitable_instance)
            instances_with_run_results.append(self._get_run_results(workload, suitable_instance, env))

        return self.policy.choose_best_instance(instances_with_run_results)
