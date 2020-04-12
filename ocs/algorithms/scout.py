import numpy.random as random
import numpy as np

from core.algorithm import Algorithm
from core.policy import Policy
from core.instance import Instance


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

            if len(suitable_instances) == 1:
                break

            best_instance = self.select_best_instance(suitable_instances, workload, env)

        return  best_instance

    def find_suitable_instances(self, best_instance, workload, env):
        suitable_instances = [best_instance]

        avaliable_instances = env.get_avaliable_instances()

        for instance in avaliable_instances:
            probability = self.estimate_probability(best_instance, instance)

            print('candidate', instance, 'with probability', probability)
            if probability > self.probability_threshold:
                suitable_instances.append(instance)

        return suitable_instances

    # returns probability that candidate instance will be better than best instance
    def estimate_probability(self, best_instance, candidate):
        cost_diff = -(best_instance.cost_per_second - candidate.cost_per_second)

        diff_sum = 0.0
        for coordinate in Instance.coordinates():
            # TODO(nmikhaylov): add weight for coordinate
            diff_sum += getattr(best_instance, coordinate) - getattr(candidate, coordinate)

        weighted_diff = diff_sum * cost_diff * 10000

        return 1 / (1 + np.exp(-weighted_diff))

    def select_best_instance(self, suitable_instances, workload, env):
        instances_with_run_results = []

        for suitable_instance in suitable_instances:
            print('try', suitable_instance)
            instances_with_run_results.append(env.run_workload_on_instance(
                workload,
                suitable_instance,
                self.runs_per_instance
            ))

        return self.policy.choose_best_instance(instances_with_run_results)
