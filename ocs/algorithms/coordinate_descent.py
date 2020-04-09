import numpy.random as random

from core.algorithm import Algorithm
from core.policy import Policy


# TODO(nmikhaylov): unit-tests?
def find_suitable_instances(avaliable_instances, best_coordinates):
    for instance in avaliable_instances:
        best_cpu = best_coordinates['n_cpu']
        best_ram = best_coordinates['n_ram_gb']

        if (best_cpu == None or best_cpu == instance.n_cpu) and (best_ram == None or best_ram == instance.n_ram_gb):
            yield instance


class CoordinateDescent(Algorithm):

    def __init__(self, config):
        self.runs_per_instance = config['runs_per_instance']
        self.seed = config['seed']
        self.policy = Policy(config['policy'])

    def choose_best_instance(self, workload, env):
        random.seed(self.seed)

        avaliable_instances = env.get_avaliable_instances()

        # TODO(nmikhaylov): remove hardcode
        value_by_coordinate = {
            'n_cpu': set(),
            'n_ram_gb': set(),
        }

        for instance in avaliable_instances:
            value_by_coordinate['n_cpu'].add(instance.n_cpu)
            value_by_coordinate['n_ram_gb'].add(instance.n_ram_gb)

        print('search space ', value_by_coordinate)

        coordinates = list(value_by_coordinate.keys())
        random.shuffle(coordinates)

        best_coordinates = {}
        for coordinate in coordinates:
            best_coordinates[coordinate] = None

        best_instance = None
        for coordinate in coordinates:
            instances_with_run_results = []
            for coordinate_value in value_by_coordinate[coordinate]:
                best_coordinates[coordinate] = coordinate_value
                suitable_instances = find_suitable_instances(avaliable_instances, best_coordinates)
                for suitable_instance in suitable_instances:
                    print('test suitable_instance', suitable_instance)
                    instances_with_run_results.append(self._get_run_results(workload, suitable_instance, env))

            if len(instances_with_run_results) == 0:
                print('not found any suitable_instance for coordinate: ', coordinate)
                break

            best_instance = self.policy.choose_best_instance(instances_with_run_results)
            best_coordinates[coordinate] = best_instance.getattr(coordinate)

        print('best coordinates is', best_coordinates)
        return best_instance
