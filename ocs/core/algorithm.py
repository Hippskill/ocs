from abc import ABC, abstractmethod


class Algorithm(ABC):

    @abstractmethod
    def choose_best_instance(self, workload, env):
        pass
