class RunResult:

    def __init__(self, elapsed_time, cost, container_metrics):
        self.elapsed_time = elapsed_time
        self.cost = cost
        self.container_metrics = container_metrics

    def __str__(self):
        return '{{ elapsed_time: {} cost: {} container_metrics: {} }}'.format(
            self.elapsed_time,
            self.cost,
            self.container_metrics
        )
