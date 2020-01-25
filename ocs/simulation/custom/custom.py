from core.instance import Instance


def load_instaces(config):
    simulation_cost = config['costs']
    simulation_limits = config['limits']
    instances = []
    for n_cpu in range(1, int(simulation_limits['max_cpu']) + 1):
        for n_ram_gb in range(1, int(simulation_limits['max_ram_gb']) + 1):
            cost_per_second = n_cpu * simulation_cost['cpu_core'] + n_ram_gb * simulation_cost['ram_gb']
            instances.append(Instance('custom', n_cpu, n_ram_gb, cost_per_second))
    return instances
