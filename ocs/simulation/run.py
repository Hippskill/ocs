#!/usr/bin/env python3
import argparse
import docker
import time
import yaml

import numpy as np

from docker_utils import run_container


def run(config):
    print(config)

    client = docker.from_env()

    simulation_cost = config['simulation']['costs']
    simulation_limits = config['simulation']['limits']
    workload = config['workload']
    algrotihm = config['algorithm']

    print('start optimizing configuration for', workload['name'])
    for n_cpu in range(4, int(simulation_limits['max_cpu']) + 1):
        for n_ram_gb in range(1, int(simulation_limits['max_ram_gb']) + 1):
            cost_per_second = n_cpu * simulation_cost['cpu_core'] + n_ram_gb * simulation_cost['ram_gb']
            print('try instance with cpu={} ram_gb={} cost_per_second={}'.format(n_cpu, n_ram_gb, cost_per_second))
            metrics = []

            for attempt in range(algrotihm['episodes']):
                start_time = time.time()

                # TODO(nmikhaylov): docker kill on ctrl+c
                container_id = run_container(
                    image=workload['image'],
                    cpuset_cpus=','.join(map(str, range(n_cpu))),
                    memory=n_ram_gb * 1024 * 1024 * 1024
                )
                while True:
                    container = client.containers.get(container_id[:12])
                    if container.status != 'running':
                        break
                    time.sleep(0.1)
                finish_time = time.time()
                elapsed = finish_time - start_time

                # TODO(nmikhaylov): use container stats as metrics
                metrics.append(elapsed)

                print('attempt={} time elapsed: {}'.format(attempt, elapsed))

            print('average time', np.mean(metrics))
            print('average cost', np.mean(metrics) * cost_per_second)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', required=True)

    args = parser.parse_args()

    with open(args.config, 'r') as yaml_config:
        config = yaml.load(yaml_config)
        run(config)


if __name__ == '__main__':
    main()
