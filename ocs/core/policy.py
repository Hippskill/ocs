class Policy:

    def __init__(self, config):
        self.config = config

    def choose_best_instance(self, instances_with_run_results):
        # ¯\_(ツ)_/¯
        return instances_with_run_results[0].instance
