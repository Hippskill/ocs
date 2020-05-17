from abc import ABC, abstractmethod

from core.instance_with_run_results import InstanceWithRunResults


class Algorithm(ABC):

    @abstractmethod
    def choose_best_instance(self, policy, workload, env):
        pass
