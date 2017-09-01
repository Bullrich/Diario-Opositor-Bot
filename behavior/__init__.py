import database
import database.firebase_crud
import rss
import rss.rss_search
from behavior.commenter.comment_formatter import set_signature
from behavior.reddit import reddit_reader


def set_verbose():
    rss.verbose = True
    database.verbose = True


def get_articles(title):
    return rss.rss_search.get_articles(title)


def get_all_comments():
    return database.firebase_crud.get_all()


def add_comment_id(comment_id):
    database.firebase_crud.add_id(comment_id)


def set_signature(signature):
    set_signature(signature)


def start_reading_process(repeat, username, subreddit):
    reddit_reader.start_reading_process(repeat, username, subreddit)
