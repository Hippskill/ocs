#!/usr/bin/env python3
import argparse
import time
import yaml

import numpy as np

if __name__ == '__main__' and __package__ is None:
   from os import sys, path
   sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from simulation import env
from core.workload import Workload


def run(config):
    print(config)

    workload = Workload(config['workload']['image'], config['workload']['name'])
    algrotihm = config['algorithm']
    simulation = env.Simulation(config['simulation'])

    print('start optimizing configuration for', workload.name)
    for instance in simulation.get_avaliable_instances():
        print('try instance', instance)
        metrics = []

        for attempt in range(algrotihm['episodes']):
            start_time = time.time()

            metrics.append(simulation.run_workload_on_instance(workload, instance))

            finish_time = time.time()
            elapsed = finish_time - start_time

            print('attempt={} time elapsed: {}'.format(attempt, elapsed))

        print('average cost', np.mean(metrics))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', required=True)

    args = parser.parse_args()

    with open(args.config, 'r') as yaml_config:
        config = yaml.load(yaml_config)
        run(config)


if __name__ == '__main__':
    main()
