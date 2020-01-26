import numpy.random as random
from core.algorithm import Algorithm
from core.policy import Policy


class RandomSearch(Algorithm):

    def __init__(self, config):
        self.runs_per_instance = config['runs_per_instance']
        self.instances_to_evaluate = config['instances_to_evaluate']
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
            run_results = []
            for attempt in range(self.runs_per_instance):
                run_result = env.run_workload_on_instance(workload, instance)
                run_results.append(run_result)
                print('attempt: {} time elapsed: {}'.format(attempt, run_result.elapsed_time))

            instances_with_run_results.append(InstanceWithRunResults(instance, run_results))

        return self.policy.choose_best_instance(instances_with_run_results)
