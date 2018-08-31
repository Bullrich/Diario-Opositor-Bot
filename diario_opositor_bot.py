#! /usr/bin/python3

import argparse
import logging
import sys

import redis

from behavior import Behavior


class DiarioOpositorBot:
    def __init__(self, log_level=logging.DEBUG, signature=''):
        args = self.get_args()
        if args['verbose']:
            log_level = logging.DEBUG
        if args['signature']:
            signature = args['signature']

        self.logger = self.create_logger(log_level)
        if signature != '':
            self.logger.info('Signature is %s', signature)
        self.behavior = Behavior.Behavior(signature, 1)

    def get_args(self):
        parser = argparse.ArgumentParser(description='Process the commands.')
        parser.add_argument('-v', '--verbose', const=True, nargs='?', help='Be verbose with the logs')
        parser.add_argument('-s', '--signature', help='Define a signature for the bot')
        parser.add_argument('-r', '--repeat', const=True, nargs='?', help='Repeat the loops once it finish')
        return vars(parser.parse_args())

    def create_logger(self, debug_level=logging.DEBUG):
        lg = logging.getLogger()
        lg_level = debug_level
        lg.setLevel(lg_level)

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(lg_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        lg.addHandler(ch)
        return lg

    def start(self):
        from pyfiglet import Figlet
        f = Figlet(font='contessa')
        print(f.renderText('Diario Opositor Bot'))

        self.logger.info('Initializing Diario Opositor Bot!')
        self.behavior.read_and_respond()
        print('Finished a round!')

    def start_server(self):
        from time import sleep
        r = redis.StrictRedis(host="0.0.0.0", port=6379, db=0)
        rsub = r.pubsub()
        rsub.subscribe("dob-start")
        while True:
            for m in rsub.listen():
                print(m)
                if m['type'] == "message":
                    if m['data'] == b'start':
                        print('Starting bot!')
                        self.start()
                        sleep(15)
            sleep(0.5)


if __name__ == '__main__':
    print('Running bot!')
    dob = DiarioOpositorBot()
    dob.start()
