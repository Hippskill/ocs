#!/usr/bin/env python3
import argparse
import time
import yaml

import numpy as np

if __name__ == '__main__' and __package__ is None:
   from os import sys, path
   sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from simulation.env import SimulationEnv
from cloud.env import CloudEnv
from core.workload import Workload
from algorithms.random_search import RandomSearch
from algorithms.full_search import FullSearch
from algorithms.coordinate_descent import CoordinateDescent
from algorithms.scout import Scout


def algorithm_from_config(config):
    if config['type'] == 'RandomSearch':
        return RandomSearch(config)
    elif config['type'] == 'FullSearch':
        return FullSearch(config)
    elif config['type'] == 'CoordinateDescent':
        return CoordinateDescent(config)
    elif config['type'] == 'Scout':
        return Scout(config)
    else:
        raise Exception('unexpected algorithm type: {}'.format(config['type']))


def env_from_config(config):
    if config['type'] == 'Simulation':
        return SimulationEnv(config['simulation'])
    elif config['type'] == 'Cloud':
        return CloudEnv(config['cloud'])
    else:
        raise Exception('unexpected env type: {}'.format(config['type']))


def run(config):
    print(config)

    workload = Workload(config['workload']['image'], config['workload']['name'])
    algorithm = algorithm_from_config(config['algorithm'])
    env = env_from_config(config['env'])

    print('start optimizing configuration for workload:', workload)
    print('avaliable instances:', ', '.join(map(str, env.get_avaliable_instances())))

    best_instance = algorithm.choose_best_instance(workload, env)

    if best_instance is None:
        print('best instance not found :(')
        return

    print('best instance is', best_instance)
    print('best instance metrics', env.run_workload_on_instance(workload, best_instance, attempts=1))
    print('cost', env.total_cost())
    print('elapsed time', env.total_elapsed_time())


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', required=True)

    args = parser.parse_args()

    with open(args.config, 'r') as yaml_config:
        config = yaml.load(yaml_config)
        run(config)


if __name__ == '__main__':
    main()
