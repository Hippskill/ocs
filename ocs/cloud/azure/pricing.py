class Pricing:

    def __init__(self, pricing_filename):
        self._price_by_name = {}

        with open(pricing_filename) as f:
            for line in f:
                line = line.rstrip()
                if len(line) == 0:
                    continue

                name, price = line.split()
                self._price_by_name[name] = float(price) / 60 / 60

    def get_cost_per_second(self, name):
        name = str.lower(name)
        if name in self._price_by_name:
            return self._price_by_name[name]
        return None
