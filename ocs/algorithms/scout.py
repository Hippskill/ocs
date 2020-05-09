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

        self.gamma = config['gamma']

        # TODO(nmikhaylov): tweak weights by config
        self.coordinate_weight = {
            coordinate: 1.0 for coordinate in Instance.coordinates()
        }

        self.learning_rate = {
            coordinate: 1.0 for coordinate in Instance.coordinates()
        }

    def choose_best_instance(self, workload, env):
        random.seed(self.seed)

        available_instances = env.get_available_instances()

        random.shuffle(available_instances)

        best_instance = available_instances[0]
        print('start scout from', best_instance)

        for _ in range(self.iters):
            assert best_instance is not None

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
            coordinate_diff = getattr(candidate, coordinate) - getattr(best_instance, coordinate)
            diff_sum += self.coordinate_weight[coordinate] * coordinate_diff

        weighted_diff = diff_sum * cost_diff

        return 1 / (1 + np.exp(-weighted_diff))

    def select_best_instance(self, suitable_instances, workload, env):
        instances_with_run_results = []

        for suitable_instance in suitable_instances[:self.max_runs_per_iter]:
            print('try instance:', suitable_instance, 'runs_per_instance:', self.runs_per_instance)
            instances_with_run_results.append(env.run_workload_on_instance(
                workload,
                suitable_instance,
                self.runs_per_instance
            ))

            self._adjust_coordinate_weights(
                best_instance=instances_with_run_results[0],
                candidate_instance=instances_with_run_results[-1]
            )

        return self.policy.choose_best_instance(instances_with_run_results)

    def _adjust_coordinate_weights(self, best_instance, candidate_instance):
        time_diff = candidate_instance.mean_elapsed - best_instance.mean_elapsed
        cost_diff = candidate_instance.mean_cost - best_instance.mean_cost
        for coordinate in Instance.coordinates():
            coordinate_diff = getattr(candidate_instance.instance, coordinate) - getattr(best_instance.instance, coordinate)

            gradient = -coordinate_diff * time_diff * cost_diff

            print('time_diff: {} cost_diff: {} coordinate_diff: {} gradient: {}'.format(
                time_diff,
                cost_diff,
                coordinate_diff,
                gradient
            ))

            self.coordinate_weight[coordinate] += gradient * self.learning_rate[coordinate]
            self.learning_rate[coordinate] *= self.gamma
