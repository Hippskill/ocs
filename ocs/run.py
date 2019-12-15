#/usr/bin/env python3
import docker
import time

client = docker.from_env()
client.containers.run('664399089934', detach=True)

while True:
    for container in client.containers.list():
        print(container.id)
        print(container.stats(stream=False))
    time.sleep(1)
