#!/usr/bin/env python3
import argparse
from flask import make_response, request, Flask
from werkzeug.serving import make_server


class Cachelot:

    def __init__(self, host, port, working_directory):
        self.host = host
        self.port = port
        self.working_directory = working_directory

        self._init_flask_server()

    def _init_flask_server(self):
        app = Flask('cachelot')

        @app.route('/run_result', methods=['GET', 'POST'])
        def run_result_handler():
            if request.method == 'POST':
                print('got new run_result ', request.data)
            elif request.method == 'GET':
                print('requesting run_result for ', request.data)
            return ''

        self.server = make_server(self.host, self.port, app)
        self.app_context = app.app_context()
        self.app_context.push()

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
