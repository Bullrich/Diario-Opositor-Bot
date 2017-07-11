from reddit import reddit_reader
from commenter import comment_formatter
import os

repeat = os.environ.get('bot_repeat') if os.environ.get('bot_repeat') is not None else None

print 'Remember you can set your own signature by typing \"export bot_firma={your signature}\"!'
print 'Current signature: ' + comment_formatter.signature

if repeat:
    print 'The bot is set to cycle until interrupted.'
else:
    print 'The bot won\'t cycle.'
    print 'You can set the bot to cycle itself by typing \"export bot_repeat=True\"'

reddit_reader.start_reading_process(repeat, u"empleadoEstatalBot", "argentina")
