class ContainerMetrics:

    def __init__(self, cpu_stats, memory_stats):
        self.cpu_stats = cpu_stats
        self.memory_stats = memory_stats

    @staticmethod
    def from_container_stats(stats):
        return ContainerMetrics(stats['cpu_stats'], stats['memory_stats'])

    def __str__(self):
        return '{{ cpu_stats: {} memory_stats: {} }}'.format(self.cpu_stats, self.memory_stats)
