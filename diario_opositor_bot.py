#! /usr/bin/python3

import argparse
import logging
import sys
import time
from deprecated import deprecated

from behaviour import Behaviour


def get_args():
    parser = argparse.ArgumentParser(description='Process the commands.')
    parser.add_argument('-v', '--verbose', const=True, nargs='?', help='Be verbose with the logs')
    parser.add_argument('-s', '--signature', help='Define a signature for the bot')
    parser.add_argument('-r', '--repeat', const=True, nargs='?', help='Repeat the loops once it finish')
    return vars(parser.parse_args())


def create_logger(debug_level=logging.DEBUG):
    lg = logging.getLogger()
    lg_level = debug_level
    lg.setLevel(lg_level)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(lg_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    lg.addHandler(ch)
    fh = logging.FileHandler('doby.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    lg.addHandler(fh)
    lg.info('-- Starting new session at %s' % time.time())
    return lg


class DiarioOpositorBot:
    def __init__(self, log_level=logging.DEBUG, signature='', thread_safe_dict=None):
        args = get_args()
        if args['verbose']:
            log_level = logging.DEBUG
        if args['signature']:
            signature = args['signature']

        self.logger = create_logger(log_level)
        if signature != '':
            self.logger.info('Signature is %s', signature)
        self.communication_dict = thread_safe_dict
        self.behavior = Behaviour.Behavior(signature, 1, thread_safe_dict)

    def start(self):
        from pyfiglet import Figlet
        f = Figlet(font='contessa')
        print(f.renderText('Diario Opositor Bot'))

        self.logger.info('Initializing Diario Opositor Bot!')
        self.behavior.read_and_respond()
        self.behavior.status.clear_status()
        self.logger.info('Finished the round')

    @deprecated(reason='I find it easier to have one Thread spawn and die instead of recycling the thread')
    def start_server(self):
        from time import sleep
        loop = True
        import json
        while loop:
            print(json.dumps(self.communication_dict))
            current_command = self.communication_dict['command']['action']
            if current_command == 'start':
                self.logger.info('Starting bot')
                # reset command so that a loop isn't forced to loop again
                with self.communication_dict as comm_dict:
                    comm_dict['command'] = {'action': 'working'}
                self.start()
                sleep(10)
            elif current_command == 'end':
                self.behavior.status.clear_status()
                loop = False
            sleep(5)
        self.logger.info('Killing thread')
        sys.exit()


if __name__ == '__main__':
    print('Running bot!')
    dob = DiarioOpositorBot(log_level=logging.INFO, thread_safe_dict={})
    dob.start()
