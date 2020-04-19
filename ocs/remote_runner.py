#!/usr/bin/env python3
import json
import argparse

from core.instance import Instance
from core.workload import Workload
from runner.local_runner import LocalRunner


def run(args):
    local_runner = LocalRunner(json.loads(args.config))

    workload = Workload.from_json_str(args.workload)
    instance = Instance.from_json_str(args.instance)

    print(local_runner.run(workload, instance).to_json_str())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--workload', required=True)
    parser.add_argument('--instance', required=True)
    parser.add_argument('--config', required=True)

    args = parser.parse_args()

    run(args)
