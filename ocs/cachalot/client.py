import json
import requests

from core.instance_with_run_results import InstanceWithRunResults


def get_key(env_name, workload, instance):
    # TODO(nmikhaylov): implement __hash__ ?
    return '{}_{}_{}'.format(env_name, str(workload), str(instance))


class CachalotClient:

    def __init__(self, host, port):
        self.cachelot_server_url = 'http://{}:{}'.format(host, port)

        self._test_healthcheck()

    def _test_healthcheck(self):
        response = requests.get('{}/healthcheck'.format(self.cachelot_server_url))
        response.raise_for_status()

    def get(self, env_name, workload, instance):
        data = {
            'key': get_key(env_name, workload, instance)
        }
        response = requests.get(
            '{}/run_result'.format(self.cachelot_server_url),
            headers={
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
            data=json.dumps(data)
        )
        response.raise_for_status()

        response_data = response.json()
        value = response_data.get('value', None)
        if value is not None:
            return InstanceWithRunResults.from_json_str(value)
        return None

    def post(self, env_name, workload, instance, run_result):
        data = {
            'key': get_key(env_name, workload, instance),
            'value': run_result.to_json_str()
        }

        response = requests.post(
            '{}/run_result'.format(self.cachelot_server_url),
            headers={
                'Content-type': 'application/json',
            },
            data=json.dumps(data)
        )
        response.raise_for_status()
