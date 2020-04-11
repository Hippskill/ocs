from core.algorithm import Algorithm
from core.policy import Policy


class FullSearch(Algorithm):

    def __init__(self, config):
        self.runs_per_instance = config['runs_per_instance']
        self.seed = config['seed']
        self.policy = Policy(config['policy'])

    def choose_best_instance(self, workload, env):
        avaliable_instances = env.get_avaliable_instances()

        instances_with_run_results = []
        for instance in avaliable_instances:
            print('try instance', instance)
            instances_with_run_results.append(env.run_workload_on_instance(workload, instance, self.runs_per_instance))

        return self.policy.choose_best_instance(instances_with_run_results)
