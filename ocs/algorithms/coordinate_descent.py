import numpy.random as random

from core.algorithm import Algorithm
from core.policy import Policy
from core.instance import Instance


# TODO(nmikhaylov): unit-tests?
def find_suitable_instances(avaliable_instances, best_coordinates):
    for instance in avaliable_instances:
        ok = True
        for coordinate in Instance.coordinates():
            best_value = best_coordinates[coordinate]
            if best_value == None:
                continue
            if best_value != getattr(instance, coordinate):
                ok = False
                break

        if ok:
            yield instance


class CoordinateDescent(Algorithm):

    def __init__(self, config):
        self.runs_per_instance = config['runs_per_instance']
        self.seed = config['seed']
        self.policy = Policy(config['policy'])

    def choose_best_instance(self, workload, env):
        random.seed(self.seed)

        avaliable_instances = env.get_avaliable_instances()

        value_by_coordinate = {}
        for coordinate in Instance.coordinates():
            value_by_coordinate[coordinate] = set()

        for instance in avaliable_instances:
            for coordinate in Instance.coordinates():
                value_by_coordinate[coordinate].add(getattr(instance, coordinate))

        print('search space ', value_by_coordinate)

        coordinates = list(value_by_coordinate.keys())
        random.shuffle(coordinates)

        best_coordinates = {}
        for coordinate in coordinates:
            best_coordinates[coordinate] = None

        best_instance = None
        for coordinate in coordinates:
            print('search for best', coordinate)

            instances_with_run_results = []
            for coordinate_value in value_by_coordinate[coordinate]:
                best_coordinates[coordinate] = coordinate_value
                suitable_instances = find_suitable_instances(avaliable_instances, best_coordinates)
                for suitable_instance in suitable_instances:
                    print('test suitable_instance', suitable_instance)
                    instances_with_run_results.append(env.run_workload_on_instance(
                        workload,
                        suitable_instance,
                        self.runs_per_instance
                    ))
                    break

            if len(instances_with_run_results) == 0:
                print('not found any suitable_instance for coordinate: ', coordinate)
                break

            best_instance = self.policy.choose_best_instance(instances_with_run_results)
            best_coordinates[coordinate] = getattr(best_instance, coordinate)

        print('best coordinates is', best_coordinates)
        return best_instance
