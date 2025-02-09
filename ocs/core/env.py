from core.run_result import RunResult
from core.instance_with_run_results import InstanceWithRunResults


class BaseEnv:

    def __init__(self, config, cachalot):
        self._env_name = config['name']
        self._run_cache = {}
        self._total_cost = 0
        self._total_elapsed_time = 0
        self._cachalot = cachalot
        self._evaluated = set()

    def run_workload_on_instance(self, workload, instance, attempts):
        run_result = self._cachalot.get(self._env_name, workload, instance)
        if run_result is not None:
            print('got run run_result from cachalot', run_result)
            result_hash = '{}_{}'.format(workload, instance)
            if result_hash not in self._evaluated:
                self._total_elapsed_time += run_result.mean_elapsed * attempts
                self._total_cost += run_result.mean_cost * attempts
                self._evaluated.add(result_hash)
            return run_result

        run_results = []

        try:
            self._allocate_instance(workload, instance)
        except Exception as e:
            print('failed to allocate instance')
            run_results.append(RunResult(
                failure=True,
                elapsed_time=0,
                cost=0,
                container_metrics=[]
            ))
            return InstanceWithRunResults(instance, run_results)
        else:
            for attempt in range(attempts):
                run_result = self._get_run_result(
                    workload,
                    instance
                )

                self._total_elapsed_time += run_result.elapsed_time
                self._total_cost += run_result.cost

                run_results.append(run_result)
                print('attempt: {}/{} failure: {} time elapsed: {} cost: {}'.format(
                    attempt + 1,
                    attempts,
                    run_result.failure,
                    run_result.elapsed_time,
                    run_result.cost,
                ))

                # TODO(nmikhaylov): threshold for failures?
                if run_result.failure:
                    break
            self._deallocate_instance(workload, instance)

        run_result = InstanceWithRunResults(instance, run_results)
        self._cachalot.post(self._env_name, workload, instance, run_result)
        return run_result

    def total_cost(self):
        return self._total_cost

    def total_elapsed_time(self):
        return self._total_elapsed_time
