import os
import plumbum

from plumbum import FG


def make_ssh(user, address):
    vm_host = '{}@{}'.format(user, address)
    return plumbum.local['ssh']['-o', 'StrictHostKeyChecking=no'][vm_host]


def setup_vm(user, address):
    vm_host = '{}@{}'.format(user, address)

    scp = plumbum.local['scp']['-o', 'StrictHostKeyChecking=no']
    ssh = make_ssh(user, address)

    scp['cloud/scripts/setup_ocs.sh']['{}:.'.format(vm_host)] & FG
    ssh['./setup_ocs.sh'] & FG
    ssh['./ocs/ocs/cloud/scripts/install_docker.sh'] & FG
