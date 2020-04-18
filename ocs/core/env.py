from core.instance_with_run_results import InstanceWithRunResults

class BaseEnv:

    def __init__(self, config):
        self._run_cache = {}

    def run_workload_on_instance(self, workload, instance, attempts):
        # TODO(nmikhaylov): implement __hash__ ?
        cache_key = '{}_{}'.format(str(workload), str(instance))

        if cache_key in self._run_cache:
            return self._run_cache[cache_key]

        run_results = []
        for attempt in range(attempts):
            run_result = self._get_run_results(workload, instance)
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

        self._run_cache[cache_key] = InstanceWithRunResults(instance, run_results)
        return self._run_cache[cache_key]
