class Workload:

    def __init__(self, image, name):
        self.image = image
        self.name = name

    def __str__(self):
        return 'Workload(name={}, image={})'.format(
            self.name,
            self.image
        )
