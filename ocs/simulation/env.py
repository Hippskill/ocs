import docker
import time

from core.instance import Instance
from core.container_metrics import ContainerMetrics
from core.run_result import RunResult

from simulation.docker_utils import run_container

from simulation.custom import custom
from simulation.aws import aws


def parse_avaliable_instances_from_config(config):
    if config['type'] == 'custom':
        return custom.load_instaces(config)
    elif config['type'] == 'aws':
        return aws.load_instaces(config)
    else:
        raise Exception('unexpected simulation type: {}'.format(config['type']))


class Simulation:
    def __init__(self, config):
        self._docker_client = docker.from_env()

        self._avaliable_instances = parse_avaliable_instances_from_config(config)
        self._metrics_poll_interval = config['metrics_poll_interval']

    def get_avaliable_instances(self):
        return self._avaliable_instances

    def run_workload_on_instance(self, workload, instance):
        start_time = time.time()

        container_id = run_container(
            image=workload.image,
            cpuset_cpus=','.join(map(str, range(instance.n_cpu))),
            memory=instance.n_ram_gb * 1024 * 1024 * 1024
        )

        container_metrics = []
        while True:
            container = self._docker_client.containers.get(container_id[:12])
            if container.status != 'running':
                break
            container_metrics.append(ContainerMetrics.from_container_stats(
                container.stats(stream=False)
            ))
            time.sleep(self._metrics_poll_interval)

        finish_time = time.time()
        elapsed_time = finish_time - start_time
        weighted_cost = elapsed_time * instance.cost_per_second

        return RunResult(elapsed_time, weighted_cost, container_metrics)
