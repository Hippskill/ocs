#!/usr/bin/env python3
import json
import plumbum

def az_vm():
    return plumbum.local['az']['vm']


def az_group():
    return plumbum.local['az']['group']


vm_list = json.loads(az_vm()['list']())
for vm in vm_list:
    name = vm['name']
    print('stop', name)
    az_vm()['delete']['--name', name]['--resource-group', 'ocs_westus']['--yes'] & plumbum.FG()

az_group()['delete']['--name', 'ocs_westus']['--yes'] & plumbum.FG

az_group()['create']['-l', 'westus']['--name', 'ocs_westus'] & plumbum.FG
