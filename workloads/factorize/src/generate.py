import random

with open('to_factorize.in', 'w') as f:
    for i in range(10000):
        f.write('{}\n'.format(random.randint(10 ** 5, 10 ** 18)))
