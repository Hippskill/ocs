class RunResult:

    def __init__(self, failure, elapsed_time, cost, container_metrics):
        self.failure = failure
        self.elapsed_time = elapsed_time
        self.cost = cost
        self.container_metrics = container_metrics

    def __str__(self):
        return '{{ failure: {} elapsed_time: {} cost: {} container_metrics: {} }}'.format(
            self.failure,
            self.elapsed_time,
            self.cost,
            list(map(str, self.container_metrics))
        )
