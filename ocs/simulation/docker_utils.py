import plumbum

def run_container(image, cpus=None, cpuset_cpus=None):
    docker = plumbum.local['docker']['run']['--detach']

    if cpus is not None:
        docker = docker['--cpus'][cpus]

    if cpuset_cpus is not None:
        docker = docker['--cpuset-cpus'][cpuset_cpus]

    docker = docker[image]

    return docker()
