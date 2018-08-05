import redis
from threading import Thread

import time

def redis_thread(conn):
    print('Starting thread')
    r = redis.StrictRedis(host="0.0.0.0", port=6379, db=0)
    r = r.pubsub()
    r.subscribe("sms_replies")
    while True:
        time.sleep(6)
        for m in r.listen():
            if m['type'] == "message":
                print(m['data'])
                print(m)
                # from_nick, to_nick, reply_body = m['data'].split(" ", 2)
                #
                # conn.msg(to_nick, "SMS reply from %s: %s [Please do not attempt to reply to this message.]" % (from_nick, reply_body))


def start_investigation(conn=None):
    t = Thread(target=redis_thread, args=(conn,))
    t.setDaemon(True)
    t.start()
