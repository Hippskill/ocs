from core.env import BaseEnv
from cloud.azure.azure import Azure


class CloudEnv(BaseEnv):
    def __init__(self, config, cachalot):
        super().__init__(config, cachalot)
        self._cloud_provider = Azure()

    def get_available_instances(self):
        return self._cloud_provider.get_available_instances()

    def _get_run_result(self, workload, instance):
        return self._cloud_provider.get_run_result(workload, instance)
