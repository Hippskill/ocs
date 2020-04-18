from core.env import BaseEnv


class RayEnv(BaseEnv):
    def __init__(self, config):
        super().__init__(config)

        self._total_elapsed_time = 0
        self._total_cost = 0
        pass

    def get_avaliable_instances(self):
        return []

    def _get_run_results(self, workload, instance):
        # TODO(nmikhaylov): implement
        return None

    def total_cost(self):
        return self._total_cost

    def total_elapsed_time(self):
        return self._total_elapsed_time
