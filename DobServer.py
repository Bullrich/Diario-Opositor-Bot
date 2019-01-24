#!/usr/bin/python3

from datetime import datetime
from json import loads
from os import environ
from threading import Thread

from bottle import route, run, response
from redis import StrictRedis

import server
from behaviour import StatusReporter
from diario_opositor_bot import DiarioOpositorBot

redis_url = '0.0.0.0'
if 'redis' in environ:
    redis_url = environ['redis']

r = StrictRedis(host=redis_url, port=6379, db=0)
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
    r.publish("dob-start", "end")
    return 'Called death command'


@route('/status')
def status():
    stat = r.get('dob-status')
    if stat:
        decoded_status = stat.decode('utf8').replace("'", '"')
        response.content_type = 'application/json'
        return decoded_status
    else:
        return "No data"

@route('/comments')
def get_comments():
    return server.fetch_comments()


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
        doby_thread = Thread(target=dob.start_server)
        doby_thread.start()
        time.sleep(0.8)
    r.publish("dob-start", "start")


print("Starting Diario-Opositor-Bot Server at " + str(datetime.now()))

if 'PORT' in environ:
    PORT = environ['PORT']
else:
    PORT = 5000

run(host='0.0.0.0', port=PORT)
