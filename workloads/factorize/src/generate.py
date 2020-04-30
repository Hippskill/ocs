import random
import sys

random.seed(1337)

with open(sys.argv[1], 'w') as f:
    for i in range(100):
        f.write('{}\n'.format(random.randint(10 ** 5, 10 ** 18)))
