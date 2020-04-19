#!/usr/bin/env python3
import argparse
import os
import pickledb
import json
from flask import make_response, request, Flask, jsonify
from werkzeug.serving import make_server


class Cachelot:

    def __init__(self, host, port, working_directory):
        self.host = host
        self.port = port
        self.working_directory = working_directory
        if not os.path.exists(self.working_directory):
            os.makedirs(self.working_directory)

        db_path = os.path.join(self.working_directory, 'run_results.db')
        self._db = pickledb.load(db_path, False)

        self._init_flask_server()

    def _init_flask_server(self):
        app = Flask('cachelot')

        @app.route('/run_result', methods=['GET', 'POST'])
        def run_result_handler():
            if request.method == 'POST':
                self.save_run_result(request.data)
            elif request.method == 'GET':
                return self.get_run_result(request.data)

        self.server = make_server(self.host, self.port, app)
        self.app_context = app.app_context()
        self.app_context.push()

    def save_run_result(self, data_bytes):
        data = json.loads(data_bytes, encoding='utf-8')
        key = data['key']
        value = data['value']
        self._db.set(key, value)
        self._db.dump()

    def get_run_result(self, data_bytes):
        data = json.loads(data_bytes, encoding='utf-8')
        key = data['key']

        if self._db.exists(key):
            data['value'] = self._db.get(key)
        else:
            data['value'] = None

        return data

    def serve_forever(self):
        print('start serving cachelot on {}:{}'.format(self.host, self.port))
        self.server.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--host', required=False, default='127.0.0.1')
    parser.add_argument('--port', required=False, default='13866')
    parser.add_argument('--working-directory', required=False, default='/etc/ocs/cachelot')

    args = parser.parse_args()

    cachelot = Cachelot(args.host, args.port, args.working_directory)
    cachelot.serve_forever()
