import numpy as np

class InstanceWithRunResults:

    def __init__(self, instance, run_results):
        self.instance = instance

        self._run_results = run_results
        self._parse_results()

    def _parse_results(self):
        self.mean_cost = np.mean([run_result.cost for run_result in self._run_results])
        self.mean_elapsed = np.mean([run_result.elapsed_time for run_result in self._run_results])

    def __str__(self):
        return 'instance: {} mean_cost: {} mean_elapsed: {}'.format(
            self.instance,
            self.mean_cost,
            self.mean_elapsed,
        )
