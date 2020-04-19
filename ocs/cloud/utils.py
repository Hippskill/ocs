import os
import plumbum


def setup_vm(user, address):
    vm_host = '{}@{}'.format(user, address)

    scp = plumbum.local['scp']
    ssh = plumbum.local['ssh']

    scripts_dir = 'cloud/scripts'
    for script in os.listdir(scripts_dir):
        print('deploy and execute script', script)
        path_to_script = os.path.join(scripts_dir, script)
        scp[path_to_script]['{}:.'.format(vm_host)] & plumbum.FG
        ssh[vm_host]['./{}'.format(script)] & plumbum.FG
