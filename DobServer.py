#!/usr/bin/python3

import logging
from datetime import datetime
from json import dumps
from os import environ
from threading import Thread

from bottle import route, run, response, auth_basic

from behaviour import StatusReporter, ThreadSafeDict
from diario_opositor_bot import DiarioOpositorBot
from server import fetch_comments, credentials

thread_dict = ThreadSafeDict.ThreadSafeDict()
dob = None


def get_bot():
    global dob
    global thread_dict
    if dob is None:
        dob = DiarioOpositorBot(log_level=logging.DEBUG, thread_safe_dict=thread_dict)
    return dob


def check(user, pw):
    cred = credentials.fetch_credentials()
    return user == cred["username"] and pw == cred['password']


@route('/')
@route('/health')
def info():
    return "OK"


@route('/run')
@auth_basic(check)
def start_bot():
    response.content_type = 'application/json'
    if bot_running():
        response.status = 409
        return {'message': 'Bot is already running'}
    dob_bot = get_bot()
    doby_thread = Thread(target=dob_bot.start)
    doby_thread.start()
    return {'message': 'Diario Opositor Bot has started!'}


@route('/stop')
@auth_basic(check)
def stop():
    response.status = 501
    response.content_type = 'application/json'
    return {'message': 'This method hasn\'t been implement'}


@route('/status')
def status():
    global thread_dict
    response.status = 200
    print(thread_dict)
    if 'status' in thread_dict and thread_dict['status']:
        response.content_type = 'application/json'
        stat = thread_dict['status']
        return dumps(stat)
    else:
        return {'message': 'No data'}


@route('/comments')
def get_comments():
    response.content_type = 'application/json'
    return fetch_comments()


def bot_running():
    global thread_dict
    if 'status' in thread_dict and 'status' in thread_dict['status']:
        return thread_dict['status']['status'] != StatusReporter.Status.OFF.value
    return False


print("Starting Diario-Opositor-Bot Server at " + str(datetime.now()))

if 'PORT' in environ:
    PORT = environ['PORT']
else:
    PORT = 5000

run(host='0.0.0.0', port=PORT)
