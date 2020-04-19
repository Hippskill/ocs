#!/usr/bin/env python3
import json
import plumbum

def az_vm():
    return plumbum.local['az']['vm']

vm_list = json.loads(az_vm()['list']())
for vm in vm_list:
    name = vm['name']
    print('stop', name)
    az_vm()['delete']['--name', name]['--resource-group', 'ocs_westus']['--yes'] & plumbum.FG()
