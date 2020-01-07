from core import instance
from core import workload


class Simulation:
    def __init__(self, config):
        self.config = config

    def get_avaliable_instances(self):
        return []

    def run_workload_on_instance(self, workload, instance):
        pass
