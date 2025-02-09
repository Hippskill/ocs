class MinTimeCostLimitPolicy:

    def __init__(self, config):
        self.max_cost = float(config['limit'])

    def choose_best_instance(self, instances_with_run_results):
        best_candidate = None

        for instance_with_run_results in instances_with_run_results:
            if instance_with_run_results.failure:
                continue

            if instance_with_run_results.mean_cost > self.max_cost:
                continue

            if best_candidate is None or\
                    best_candidate.mean_elapsed > instance_with_run_results.mean_elapsed:
                best_candidate = instance_with_run_results

        if best_candidate is None:
            return None

        return best_candidate.instance

class MinCostTimeLimitPolicy:

    def __init__(self, config):
        self.max_time = float(config['limit'])

    def choose_best_instance(self, instances_with_run_results):
        best_candidate = None

        for instance_with_run_results in instances_with_run_results:
            if instance_with_run_results.failure:
                continue

            if instance_with_run_results.mean_elapsed > self.max_time:
                continue

            if best_candidate is None or\
                    best_candidate.mean_cost > instance_with_run_results.mean_cost:
                best_candidate = instance_with_run_results

        if best_candidate is None:
            return None

        return best_candidate.instance
