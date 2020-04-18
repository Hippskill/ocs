import json


class Instance:

    def __init__(self, name, n_cpu, n_ram_gb, cost_per_second):
        self.name = name
        self.n_cpu = n_cpu
        self.n_ram_gb = n_ram_gb
        self.cost_per_second = cost_per_second

    @staticmethod
    def coordinates():
        return ('n_cpu', 'n_ram_gb')

    def __str__(self):
        return 'Instance(name={}, n_cpu={}, n_ram_gb={}, cost_per_second={})'.format(
            self.name,
            self.n_cpu,
            self.n_ram_gb,
            self.cost_per_second
        )

    def to_json_str(self):
        instance_json = {
            'name': self.name,
            'n_cpu': self.n_cpu,
            'n_ram_gb': self.n_ram_gb,
            'cost_per_second': self.cost_per_second
        }
        return json.dumps(instance_json)

    @staticmethod
    def from_json_str(instance_json_str):
        instance_json = json.loads(instance_json_str)
        return Instance(
            name=instance_json['name'],
            n_cpu=instance_json['n_cpu'],
            n_ram_gb=instance_json['n_ram_gb'],
            cost_per_second=instance_json['cost_per_second']
        )
