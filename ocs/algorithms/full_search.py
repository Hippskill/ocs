from core.algorithm import Algorithm


class FullSearch(Algorithm):

    def __init__(self, config):
        self.runs_per_instance = config['runs_per_instance']
        self.seed = config['seed']

    def choose_best_instance(self, policy, workload, env):
        available_instances = env.get_available_instances()

        instances_with_run_results = []
        for instance in available_instances:
            print('try instance', instance)
            instances_with_run_results.append(env.run_workload_on_instance(workload, instance, self.runs_per_instance))

        return policy.choose_best_instance(instances_with_run_results)
