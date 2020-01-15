class Instance:

    def __init__(self, n_cpu, n_ram_gb, cost_per_second):
        self.n_cpu = n_cpu
        self.n_ram_gb = n_ram_gb
        self.cost_per_second = cost_per_second

    def __str__(self):
        return 'Instance(n_cpu={}, n_ram_gb={}, cost_per_second={})'.format(
            self.n_cpu,
            self.n_ram_gb,
            self.cost_per_second
        )
