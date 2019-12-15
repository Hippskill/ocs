import plumbum

def run_container(image, cpus=None):
    docker = plumbum.local['docker']['run']['--detach']

    if cpus is not None:
        docker = docker['--cpus'][cpus]

    docker = docker[image]

    return docker()
