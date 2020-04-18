from core.env import BaseEnv
from azure import Azure


class CloudEnv(BaseEnv):
    def __init__(self, config):
        super().__init__(config)

        self._total_elapsed_time = 0
        self._total_cost = 0

        self._cloud_provider = Azure()

        pass

    def get_available_instances(self):
        return []

    def _get_run_results(self, workload, instance):
        # TODO(nmikhaylov): implement
        return None

    def total_cost(self):
        return self._total_cost

    def total_elapsed_time(self):
        return self._total_elapsed_time
