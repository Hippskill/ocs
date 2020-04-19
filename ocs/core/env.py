from core.instance_with_run_results import InstanceWithRunResults

class BaseEnv:

    def __init__(self, config, cachalot):
        self._env_name = config['name']
        self._run_cache = {}
        self._total_cost = 0
        self._total_elapsed_time = 0
        self._cachalot = cachalot

    def run_workload_on_instance(self, workload, instance, attempts):
        run_result = self._cachalot.get(self._env_name, workload, instance)
        if run_result is not None:
            print('got run run_result from cachalot', run_result)
            return run_result

        run_results = []

        self._allocate_instance(workload, instance)
        for attempt in range(attempts):
            run_result = self._get_run_result(
                workload,
                instance
            )

            self._total_elapsed_time += run_result.elapsed_time
            self._total_cost += run_result.cost

            run_results.append(run_result)
            print('attempt: {} failure: {} time elapsed: {} cost: {}'.format(
                attempt,
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
