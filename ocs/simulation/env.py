import docker
import time

from core.instance import Instance
from core.container_metrics import ContainerMetrics
from simulation.docker_utils import run_container


def parse_avaliable_instances_from_config(config):
    simulation_cost = config['costs']
    simulation_limits = config['limits']
    instances = []
    for n_cpu in range(1, int(simulation_limits['max_cpu']) + 1):
        for n_ram_gb in range(1, int(simulation_limits['max_ram_gb']) + 1):
            cost_per_second = n_cpu * simulation_cost['cpu_core'] + n_ram_gb * simulation_cost['ram_gb']
            instances.append(Instance(n_cpu, n_ram_gb, cost_per_second))
    return instances


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
        weighted_cost = (finish_time - start_time) * instance.cost_per_second

        return weighted_cost, container_metrics
