import numpy.random as random

from core.algorithm import Algorithm
from core.instance import Instance


# TODO(nmikhaylov): unit-tests?
def find_suitable_instances(available_instances, best_coordinates):
    for instance in available_instances:
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

    def choose_best_instance(self, policy, workload, env):
        random.seed(self.seed)

        available_instances = env.get_available_instances()

        value_by_coordinate = {}
        for coordinate in Instance.coordinates():
            value_by_coordinate[coordinate] = set()

        for instance in available_instances:
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
                print('test coordinate_value:', coordinate_value)
                best_coordinates[coordinate] = coordinate_value
                suitable_instances = find_suitable_instances(available_instances, best_coordinates)
                for suitable_instance in suitable_instances:
                    print('test suitable_instance', suitable_instance)
                    results = env.run_workload_on_instance(
                        workload,
                        suitable_instance,
                        self.runs_per_instance
                    )

                    # allocation failed
                    if results.failure and results.mean_cost == 0.0:
                        continue

                    instances_with_run_results.append(results)
                    break

            if len(instances_with_run_results) == 0:
                print('not found any suitable_instance for coordinate: ', coordinate)
                break

            best_instance = policy.choose_best_instance(instances_with_run_results)
            best_coordinates[coordinate] = getattr(best_instance, coordinate)

        print('best coordinates is', best_coordinates)
        return best_instance
