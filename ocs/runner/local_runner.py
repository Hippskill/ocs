import time
import docker

from core.container_metrics import ContainerMetrics
from core.run_result import RunResult

from docker_helper.docker_utils import run_container


class LocalRunner:

    def __init__(self, config):
        self._docker_client = docker.from_env()
        self._metrics_poll_interval = config['metrics_poll_interval']
        self._timeout = config['timeout']

    def run(self, workload, instance):
        start_time = time.time()

        container_id = run_container(
            image=workload.image,
            cpuset_cpus=','.join(map(str, range(instance.n_cpu))),
            memory=instance.n_ram_gb * 1024 * 1024 * 1024
        )

        # TODO(nmikhaylov): string failure reason instaed of boolean flag?
        failure = False

        container_metrics = []
        while True:
            container = self._docker_client.containers.get(container_id[:12])
            if container.status != 'running':
                break

            # TODO(nmikhaylov): also handle OOM as failure
            if time.time() - start_time > self._timeout:
                container.stop()
                failure = True
                break

            container_metrics.append(ContainerMetrics.from_container_stats(
                container.stats(stream=False)
            ))
            time.sleep(self._metrics_poll_interval)

        finish_time = time.time()
        elapsed_time = finish_time - start_time
        weighted_cost = elapsed_time * instance.cost_per_second

        return RunResult(failure, elapsed_time, weighted_cost, container_metrics)
