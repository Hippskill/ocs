import plumbum


def run_container(image, cpuset_cpus=None, memory=None):
    docker = plumbum.local['docker']['run']['--detach']

    if cpuset_cpus is not None:
        docker = docker['--cpuset-cpus'][cpuset_cpus]

    if memory is not None:
        docker = docker['--memory'][memory]

    docker = docker[image]

    return docker()
