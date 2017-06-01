from reddit import reddit_reader

print 'Remember you can set your own signature by typing \"export bot_firma={your signature}\"!'
print 'Current signature: ' + reddit_reader.signature

reddit_reader.start_reading_process()
