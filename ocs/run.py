#!/usr/bin/env python3
import docker
import time

from simulation.docker_utils import run_container

client = docker.from_env()

start_time = time.time()
container_id = run_container(image='2e1f31450d9f', cpuset_cpus='1,2,3')
while True:
    container = client.containers.get(container_id[:12])
    if container.status != 'running':
        break
    print(container.id)
    print(container.stats(stream=False))
    time.sleep(1)
finish_time = time.time()
print('time elapsed: {}'.format(finish_time - start_time))
