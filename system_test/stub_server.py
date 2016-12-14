# -*- coding: utf-8 -*-
"""HTTP Stub server"""

import logging
import random
import sys
import time

from flask import jsonify, Flask
from werkzeug import exceptions as http_errors

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
)
app = Flask('stub_server')


@app.route('/')
def index():
    return jsonify({'status': 'ok'})


@app.route('/long/<int:sleep>')
def long(sleep):
    time.sleep(sleep)
    return jsonify({'status': 'ok', 'slept': sleep})


@app.route('/error/<int:code>')
def error(code):
    return jsonify({'status': 'error'}), code


class RandomFunctions(object):
    """Set of random test functions"""

    @staticmethod
    def random_sleep():
        sleep = random.randint(1, 10)
        time.sleep(sleep)
        return jsonify({'status': 'ok', 'slept': sleep})

    @staticmethod
    def random_status_code():
        error_class = getattr(http_errors, random.choice(http_errors.__all__))
        raise error_class()


@app.route('/random')
def random_view():
    methods = [
        RandomFunctions.random_sleep,
        RandomFunctions.random_status_code,
    ]
    m = random.choice(methods)
    return m()


if __name__ == '__main__':
    port = 8080
    if len(sys.argv) > 1:
        port = sys.argv[1]
    app.run(port=port)
