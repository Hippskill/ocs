import json
import plumbum
import time

from cloud.azure.pricing import Pricing
from cloud.utils import setup_vm, make_ssh
from core.instance import Instance
from core.run_result import RunResult


def az():
    return plumbum.local['az']


def az_vm():
    return az()['vm']


def get_ip_addres(vm_name):
    #TODO(nmikhaylov): add limit for iterations
    while True:
        ip_info = json.loads(az_vm()['list-ip-addresses'] \
            ['--resource-group', 'ocs_westus'] \
            ['--name', vm_name]())

        if len(ip_info) != 0:
            return ip_info[0]['virtualMachine']['network']['publicIpAddresses'][0]['ipAddress']

        time.sleep(10)


def parse_instances(pricing, list_sizes_json, max_cpu, max_ram):
    available_instances = []
    for size in list_sizes_json:
        name = size['name']
        cost_per_second = pricing.get_cost_per_second(name)

        if cost_per_second is None:
            print('skip {}, price not found'.format(name))
            continue

        n_cpu = int(size['numberOfCores'])
        n_ram_gb = int(size['memoryInMb']) // 1024

        if n_cpu > max_cpu or n_ram_gb > max_ram:
            continue

        available_instances.append(Instance(
            name=name,
            n_cpu=n_cpu,
            n_ram_gb=n_ram_gb,
            cost_per_second=cost_per_second
        ))
        print(str(available_instances[-1]))
    return available_instances


class Azure:
    def __init__(self, config):
        self._pricing = Pricing(config['pricing'])
        self._available_instances = None
        self._config_str = json.dumps(config)
        self._max_cpu = config['max_cpu']
        self._max_ram = config['max_ram']

    def get_available_instances(self):
        if self._available_instances is not None:
            return self._available_instances

        #TODO(nmikhaylov): -l to config
        list_sizes_json = json.loads(az_vm()['list-sizes']['-l']['westus']())
        self._available_instances = parse_instances(self._pricing, list_sizes_json, self._max_cpu, self._max_ram)
        return self._available_instances

    def allocate_instance(self, workload, instance):
        vm_name = 'vm_{}_{}'.format(workload.name, instance.name)

        create_vm = az_vm()['create'] \
            ['--resource-group', 'ocs_westus'] \
            ['--name', vm_name] \
            ['--image', 'UbuntuLTS'] \
            ['--admin-username', 'azureuser'] \
            ['--generate-ssh-keys'] \
            ['--size', instance.name]
        create_vm & plumbum.FG

        ip_address = get_ip_addres(vm_name)

        setup_vm(user='azureuser', address=ip_address)

    def deallocate_instance(self, workload, instance):
        vm_name = 'vm_{}_{}'.format(workload.name, instance.name)

        az_vm()['delete'] \
            ['--resource-group', 'ocs_westus'] \
            ['--name', vm_name] \
            ['--yes'] & plumbum.FG

    def get_run_result(self, workload, instance):
        vm_name = 'vm_{}_{}'.format(workload.name, instance.name)
        ip_address = get_ip_addres(vm_name)

        ssh = make_ssh(user='azureuser', address=ip_address)

        remote_runner_cmd = 'sudo ./ocs/ocs/remote_runner.py --workload \'{}\' --instance \'{}\' --config \'{}\''.format(
            workload.to_json_str(),
            instance.to_json_str(),
            self._config_str
        )
        run_result_str = ssh[remote_runner_cmd]()
        run_result = RunResult.from_json_str(run_result_str)
        return run_result
