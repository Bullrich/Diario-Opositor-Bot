#!/usr/bin/python3

from diario_opositor_bot import DiarioOpositorBot, get_status
import threading
from datetime import datetime
import redis
from bottle import route, run, template

dob_thread = None
r = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)


@route('/run')
def run_bot():
    global dob_thread
    if dob_thread is None or not dob_thread.is_alive():
        import logging
        dob = DiarioOpositorBot(log_level=logging.INFO)
        dob_thread = threading.Thread(target=dob.start_server)
        dob_thread.start()
    if bot_running() is False:
        r.publish("dob-start", "start")
        return 'Starting Diario Opositor Bot'
    else:
        return 'Diario Opositor Bot is already running'


@route('/stop')
def stop():
    return 'Not implemented yet'


@route('/status')
def status():
    if bot_running():
        return 'Bot is running'
    else:
        return 'Bot is NOT running'


def bot_running():
    return r.get('dob-running') == b'True'


print("Starting Diario-Opositor-Bot Server at " + str(datetime.now()))

run(host='0.0.0.0', port=7999)
