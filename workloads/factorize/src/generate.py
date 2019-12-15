import random
import sys

with open(sys.argv[1], 'w') as f:
    for i in range(1000):
        f.write('{}\n'.format(random.randint(10 ** 5, 10 ** 18)))
