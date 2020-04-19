import json
import numpy as np

from core.instance import Instance
from core.run_result import RunResult


class InstanceWithRunResults:

    def __init__(self, instance, run_results):
        self.instance = instance

        self._run_results = run_results
        self._parse_results()

    def _parse_results(self):
        self.failure = any([run_result.failure for run_result in self._run_results])
        self.mean_cost = np.mean([run_result.cost for run_result in self._run_results])
        self.mean_elapsed = np.mean([run_result.elapsed_time for run_result in self._run_results])

    def __str__(self):
        return 'instance: {} failure: {} mean_cost: {} mean_elapsed: {}'.format(
            self.instance,
            self.failure,
            self.mean_cost,
            self.mean_elapsed,
        )

    def to_json_str(self):
        return json.dumps({
            'instance': self.instance.to_json_str(),
            'failure': self.failure,
            'mean_cost': self.mean_cost,
            'mean_elapsed': self.mean_elapsed
        })

    @staticmethod
    def from_json_str(json_str):
        data = json.loads(json_str)
        return InstanceWithRunResults(
            Instance.from_json_str(data['instance']),
            run_results=[
                RunResult(
                    failure=bool(data['failure']),
                    elapsed_time=float(data['mean_elapsed']),
                    cost=float(data['mean_cost']),
                    container_metrics={}
                )
            ]
        )
