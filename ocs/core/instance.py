class Instance:

    def __init__(self, name, n_cpu, n_ram_gb, cost_per_second):
        self.name = name
        self.n_cpu = n_cpu
        self.n_ram_gb = n_ram_gb
        self.cost_per_second = cost_per_second

    def __str__(self):
        return 'Instance(name={}, n_cpu={}, n_ram_gb={}, cost_per_second={})'.format(
            self.name,
            self.n_cpu,
            self.n_ram_gb,
            self.cost_per_second
        )
