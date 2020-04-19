from core.env import BaseEnv
from cloud.azure.azure import Azure


class CloudEnv(BaseEnv):
    def __init__(self, config, cachalot):
        super().__init__(config, cachalot)
        self._cloud_provider = Azure(config['azure'])

    def get_available_instances(self):
        return self._cloud_provider.get_available_instances()

    def _allocate_instance(self, workload, instance):
        return self._cloud_provider.allocate_instance(workload, instance)

    def _deallocate_instance(self, workload, instance):
        return self._cloud_provider.deallocate_instance(workload, instance)

    def _get_run_result(self, workload, instance):
        return self._cloud_provider.get_run_result(workload, instance)
