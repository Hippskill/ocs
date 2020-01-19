import pandas as pd

from core.instance import Instance

def load_instaces(config):
    aws_data = pd.read_csv(config['aws_data_path'])

    instances = []
    for row in aws_data.iterrows():
        n_cpu = row[1]['cpu']
        n_ram_gb = row[1]['memory']
        cost_per_second = row[1]['cost']
        instances.append(Instance(n_cpu, n_ram_gb, cost_per_second))

    return instances
