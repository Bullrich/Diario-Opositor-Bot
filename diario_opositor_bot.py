#! /usr/bin/python

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import behavior

repeat = None

print sys.argv[0]
for arg in sys.argv:
    if arg == sys.argv[0]:
        pass
    elif arg == '-v':
        print 'verbose mode'
        behavior.set_verbose()
    elif arg == '--signature' or arg == '-s':
        signature = raw_input("Please write the bot's signature:\n")
        behavior.set_signature(signature)
        print "Your signature is: \"" + signature + "\""
    elif arg == '--repeat' or arg == "-r":
        repeat = True
    else:
        print "Command not found"
        exit()

if repeat:
    print 'The bot is set to cycle until interrupted.'
else:
    print 'The bot won\'t cycle.'
    print 'You can set the bot to cycle itself by passing the parameter --repeat'

behavior.start_reading_process(repeat, u"empleadoEstatalBot", "argentina")
