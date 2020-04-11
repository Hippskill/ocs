import numpy.random as random

from core.algorithm import Algorithm
from core.policy import Policy


class RandomSearch(Algorithm):

    def __init__(self, config):
        self.instances_to_evaluate = config['instances_to_evaluate']

        self.runs_per_instance = config['runs_per_instance']
        self.seed = config['seed']
        self.policy = Policy(config['policy'])

    def choose_best_instance(self, workload, env):
        random.seed(self.seed)

        avaliable_instances = env.get_avaliable_instances()
        random_instaces_indeces = random.choice(
            len(avaliable_instances),
            self.instances_to_evaluate,
            replace=False
        )

        instances_with_run_results = []
        for instance_id in random_instaces_indeces:
            instance = avaliable_instances[instance_id]
            print('try instance', instance)
            instances_with_run_results.append(env.run_workload_on_instance(workload, instance, self.runs_per_instance))

        return self.policy.choose_best_instance(instances_with_run_results)
