import plumbum


def run_container(image, cpuset_cpus=None, memory_mb=None):
    docker = plumbum.local['docker']['run']['--detach']

    if cpuset_cpus is not None:
        docker = docker['--cpuset-cpus'][cpuset_cpus]

    if memory_mb is not None:
        docker = docker['--memory', '{}m'.format(memory_mb)]
        docker = docker['--memory-swappiness', 0]

    docker = docker[image]

    return docker()
