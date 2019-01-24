import time
from behaviour.database import FirebaseController
from behaviour.config import fetch_credentials

database = FirebaseController.FirebaseController(fetch_credentials()['firebase'])
all_comments = {}
last_comment_check = 0


def minutes_passed(old_epoch, minutes):
    return time.time() - old_epoch >= (minutes * 60)


def fetch_comments():
    global all_comments
    # Stop from pinging firebase all the time
    if minutes_passed(last_comment_check, 5):
        all_comments = database.get_raw_comments()
    return all_comments
