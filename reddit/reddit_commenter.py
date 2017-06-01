# coding=utf-8
import os

fileWithComments = "comments_replied_to.txt"


def get_saved_comments():
    if not os.path.isfile(fileWithComments):
        old_comments = []
    else:
        with open(fileWithComments, "r") as f:
            saved_comments = f.read()
            old_comments = saved_comments.split("\n")
            old_comments = filter(None, old_comments)

    return old_comments


def reply_to_comment(comment, comment_body):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    comment.reply(comment_body)


def save_comment_id_to_file(comment_id):
    with open(fileWithComments, "a") as f:
        f.write(comment_id + "\n")
