from abc import ABC, abstractmethod

from core.instance_with_run_results import InstanceWithRunResults


class Algorithm(ABC):

    @abstractmethod
    def choose_best_instance(self, workload, env):
        pass

    def _get_run_results(self, workload, instance, env):
        run_results = []
        for attempt in range(self.runs_per_instance):
            run_result = env.run_workload_on_instance(workload, instance)
            run_results.append(run_result)
            print('attempt: {} time elapsed: {}'.format(attempt, run_result.elapsed_time))

        return InstanceWithRunResults(instance, run_results)
