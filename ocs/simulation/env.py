from core.instance import Instance
from core.env import BaseEnv

from simulation.custom import custom
from simulation.aws import aws

from runner.local_runner import LocalRunner


def parse_available_instances_from_config(config):
    if config['type'] == 'custom':
        return custom.load_instaces(config)
    elif config['type'] == 'aws':
        return aws.load_instaces(config)
    else:
        raise Exception('unexpected simulation type: {}'.format(config['type']))


class SimulationEnv(BaseEnv):

    def __init__(self, config, cachalot):
        super().__init__(config, cachalot)

        self._local_runner = LocalRunner(config)
        self._available_instances = parse_available_instances_from_config(config)
        self._run_cache = {}

    def get_available_instances(self):
        return self._available_instances

    def _allocate_instance(self, workload, instance):
        pass

    def _deallocate_instance(self, workload, instance):
        pass

    def _get_run_result(self, workload, instance):
        return self._local_runner.run(workload, instance)
