#! /usr/bin/python

import sys
import logging
from behavior import Behavior
import argparse

running = False


class DiarioOpositorBot:
    def __init__(self, log_level=logging.INFO, signature=''):
        print('Bot iniciado')
        args = self.get_args()
        if args['verbose']:
            log_level = logging.DEBUG
        if args['signature']:
            signature = args['signature']

        self.logger = self.create_logger(log_level)
        if signature != '':
            self.logger.info('Signature is %s', signature)
        self.behavior = Behavior.Behavior(signature, 0)

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
        global running
        running = True
        self.behavior.read_and_respond()
        print('Finished a round!')
        running = False


if __name__ == '__main__':
    print('Running bot!')
    dob = DiarioOpositorBot()
    dob.start()


def get_status():
    global running
    return running
