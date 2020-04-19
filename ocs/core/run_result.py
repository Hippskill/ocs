import json


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

    def to_json_str(self):
        return json.dumps({
            'failure': self.failure,
            'elapsed_time': self.elapsed_time,
            'cost': self.cost
        })

    @staticmethod
    def from_json_str(data_str):
        data = json.loads(data_str)
        return RunResult(
            failure=bool(data['failure']),
            elapsed_time=float(data['elapsed_time']),
            cost=float(data['cost']),
            container_metrics=[]
        )
