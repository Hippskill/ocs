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

    print('start optimizing configuration for workload: ', workload)
    for instance in simulation.get_avaliable_instances():
        print('try instance', instance)

        run_results = []
        for attempt in range(algrotihm['episodes']):
            run_result = simulation.run_workload_on_instance(workload, instance)

            run_results.append(run_result)

            print('attempt: {} time elapsed: {}'.format(attempt, run_result.elapsed_time))

        print('mean_cost: {}'.format(np.mean([run_result.cost for run_result in run_results])))


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', required=True)

    args = parser.parse_args()

    with open(args.config, 'r') as yaml_config:
        config = yaml.load(yaml_config)
        run(config)


if __name__ == '__main__':
    main()
