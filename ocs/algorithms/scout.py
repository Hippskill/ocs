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
        self.max_runs_per_iter = config['max_runs_per_iter']
        self.cost_adjust_coef = config['cost_adjust_coef']

    def choose_best_instance(self, workload, env):
        random.seed(self.seed)

        available_instances = env.get_available_instances()

        random.shuffle(available_instances)

        best_instance = available_instances[0]
        print('start scout from', best_instance)

        for _ in range(self.iters):
            suitable_instances = self.find_suitable_instances(best_instance, workload, env)

            if len(suitable_instances) == 1:
                break

            best_instance = self.select_best_instance(suitable_instances, workload, env)

        return  best_instance

    def find_suitable_instances(self, best_instance, workload, env):
        suitable_instances = [(best_instance, 1.0)]

        available_instances = env.get_available_instances()

        for instance in available_instances:
            probability = self.estimate_probability(best_instance, instance)

            print('candidate', instance, 'with probability', probability)
            if probability > self.probability_threshold:
                suitable_instances.append([instance, probability])

        suitable_instances.sort(key=lambda x: -x[1])
        return [suitable_instance[0] for suitable_instance in suitable_instances]

    # returns probability that candidate instance will be better than best instance
    def estimate_probability(self, best_instance, candidate):
        cost_diff = (candidate.cost_per_second - best_instance.cost_per_second) * self.cost_adjust_coef

        diff_sum = 0.0
        for coordinate in Instance.coordinates():
            # TODO(nmikhaylov): add weight for coordinate
            diff_sum += getattr(candidate, coordinate) - getattr(best_instance, coordinate)

        weighted_diff = diff_sum * cost_diff

        return 1 / (1 + np.exp(-weighted_diff))

    def select_best_instance(self, suitable_instances, workload, env):
        instances_with_run_results = []

        for suitable_instance in suitable_instances[:self.max_runs_per_iter]:
            print('try', suitable_instance)
            instances_with_run_results.append(env.run_workload_on_instance(
                workload,
                suitable_instance,
                self.runs_per_instance
            ))

        return self.policy.choose_best_instance(instances_with_run_results)
