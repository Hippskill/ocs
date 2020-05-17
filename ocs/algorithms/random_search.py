import numpy.random as random

from core.algorithm import Algorithm


class RandomSearch(Algorithm):

    def __init__(self, config):
        self.iters = config['iters']
        self.runs_per_instance = config['runs_per_instance']
        self.seed = config['seed']

    def choose_best_instance(self, policy, workload, env):
        random.seed(self.seed)

        available_instances = env.get_available_instances()
        random_instaces_indeces = random.choice(
            len(available_instances),
            self.iters,
            replace=False
        )

        instances_with_run_results = []
        for instance_id in random_instaces_indeces:
            instance = available_instances[instance_id]
            print('try instance', instance)
            instances_with_run_results.append(env.run_workload_on_instance(workload, instance, self.runs_per_instance))

        return policy.choose_best_instance(instances_with_run_results)
