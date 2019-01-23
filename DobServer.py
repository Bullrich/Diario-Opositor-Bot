#!/usr/bin/python3

import os
import threading
from datetime import datetime
from json import loads
from os import environ

import redis
from bottle import route, run, response

from behavior import StatusReporter
from diario_opositor_bot import DiarioOpositorBot

redis_url = '0.0.0.0'
redis_env = environ['redis']
if redis_env:
    redis_url = redis_env

r = redis.StrictRedis(host=redis_url, port=6379, db=0)
r.delete('dob-status')


@route('/run')
def run_bot():
    response.content_type = 'application/json'
    if bot_running():
        return {'success': False, 'message': 'Diario Opositor Bot is already running'}
    else:
        start_bot()
        return {'success': True, 'message': 'Starting Diario Opositor Bot'}


@route('/stop')
def stop():
    return 'Not implemented yet'


@route('/status')
def status():
    stat = r.get('dob-status')
    if stat:
        decoded_status = stat.decode('utf8').replace("'", '"')
        response.content_type = 'application/json'
        return decoded_status
    else:
        return "No data"


def bot_running():
    stat = r.get('dob-status')
    if stat:
        bot_status = stat.decode('utf8').replace("'", '"')
        js_status = loads(bot_status)
        return js_status['status'] != StatusReporter.Status.OFF.value
    return False


def start_bot():
    if r.get('dob-status') is None:
        import logging
        import time
        dob = DiarioOpositorBot(log_level=logging.INFO, redis_url=redis_url)
        doby_thread = threading.Thread(target=dob.start_server)
        doby_thread.start()
        time.sleep(0.8)
    r.publish("dob-start", "start")


print("Starting Diario-Opositor-Bot Server at " + str(datetime.now()))

if 'PORT' in os.environ:
    PORT = os.environ['PORT']
else:
    PORT = 5000

run(host='0.0.0.0', port=PORT)
