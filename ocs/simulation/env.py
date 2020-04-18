import docker
import time

from core.instance import Instance
from core.container_metrics import ContainerMetrics
from core.run_result import RunResult
from core.env import BaseEnv

from simulation.docker_utils import run_container

from simulation.custom import custom
from simulation.aws import aws


def parse_available_instances_from_config(config):
    if config['type'] == 'custom':
        return custom.load_instaces(config)
    elif config['type'] == 'aws':
        return aws.load_instaces(config)
    else:
        raise Exception('unexpected simulation type: {}'.format(config['type']))


class SimulationEnv(BaseEnv):

    def __init__(self, config):
        super().__init__(config)

        self._docker_client = docker.from_env()

        self._available_instances = parse_available_instances_from_config(config)
        self._metrics_poll_interval = config['metrics_poll_interval']
        self._timeout = config['timeout']
        self._total_elapsed_time = 0
        self._total_cost = 0
        self._run_cache = {}

    def get_available_instances(self):
        return self._available_instances

    def _get_run_results(self, workload, instance):
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

        self._total_elapsed_time += elapsed_time
        self._total_cost += weighted_cost

        return RunResult(failure, elapsed_time, weighted_cost, container_metrics)

    def total_cost(self):
        return self._total_cost

    def total_elapsed_time(self):
        return self._total_elapsed_time
