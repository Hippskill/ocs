import json


class Workload:

    def __init__(self, image, name):
        self.image = image
        self.name = name

    def __str__(self):
        return 'Workload(name={}, image={})'.format(
            self.name,
            self.image
        )

    def to_json_str(self):
        workload_json = {
            'image': self.image,
            'name': self.name
        }
        return json.dumps(workload_json)

    @staticmethod
    def from_json_str(workload_json_str):
        workload_json = json.loads(workload_json_str)
        return Workload(
            image=workload_json['image'],
            name=workload_json['name']
        )
