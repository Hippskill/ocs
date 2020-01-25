import pandas as pd

from core.instance import Instance


def parse_memory(raw):
    assert str.endswith(raw, 'GiB')
    return float(raw[:-4])


def parse_cost(raw):
    assert raw[0] == '$'
    return float(raw[1:])


def load_instaces(config):
    aws_data = pd.read_csv(config['aws_data_path'])
    limits = config['limits']

    instances = []
    for row in aws_data.iterrows():
        name = row[1]['name']

        n_cpu = row[1]['cpu']
        if n_cpu > limits['max_cpu']:
            continue

        n_ram_gb = parse_memory(row[1]['memory'])
        if n_ram_gb > limits['max_ram_gb']:
            continue

        cost_per_second = parse_cost(row[1]['cost']) / 60
        instances.append(Instance(name, n_cpu, n_ram_gb, cost_per_second))

    return instances
