import json
import plumbum

from core.instance import Instance

def az():
    return plumbum.local['az']


def az_vm():
    return az()['vm']


def parse_instances(list_sizes_json):
    available_instances = []
    for size in list_sizes_json:
        print(size)
        available_instances.append(Instance(
            name=size['name'],
            n_cpu=int(size['numberOfCores']),
            n_ram_gb=int(size['memoryInMb']) // 1024,
            # TODO(nmikhaylov): find cost
            cost_per_second=0.0
        ))
        print(str(available_instances[-1]))
    return available_instances


class Azure:
    def __init__(self):
        self._available_instances = None

    def get_available_instances(self):
        if self._available_instances is not None:
            return self._available_instances

        #TODO(nmikhaylov): -l to config
        list_sizes_json = json.loads(az_vm()['list-sizes']['-l']['westus']())
        self._available_instances = parse_instances(list_sizes_json)
        return self._available_instances

    def get_run_result(workload, instance):
        return None
