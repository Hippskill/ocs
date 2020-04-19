import json
import plumbum

from cloud.azure.pricing import Pricing
from core.instance import Instance

def az():
    return plumbum.local['az']


def az_vm():
    return az()['vm']


def parse_instances(pricing, list_sizes_json):
    available_instances = []
    for size in list_sizes_json:
        name = size['name']
        cost_per_second = pricing.get_cost_per_second(name)

        if cost_per_second is None:
            print('skip {}, price not found'.format(name))
            continue

        available_instances.append(Instance(
            name=name,
            n_cpu=int(size['numberOfCores']),
            n_ram_gb=int(size['memoryInMb']) // 1024,
            cost_per_second=cost_per_second
        ))
        print(str(available_instances[-1]))
    return available_instances


class Azure:
    def __init__(self, config):
        self._pricing = Pricing(config['pricing'])
        self._available_instances = None

    def get_available_instances(self):
        if self._available_instances is not None:
            return self._available_instances

        #TODO(nmikhaylov): -l to config
        list_sizes_json = json.loads(az_vm()['list-sizes']['-l']['westus']())
        self._available_instances = parse_instances(self._pricing, list_sizes_json)
        return self._available_instances

    def get_run_result(self, workload, instance):
        return None
