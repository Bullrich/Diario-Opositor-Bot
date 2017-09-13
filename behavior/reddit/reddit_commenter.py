# coding=utf-8


def reply_to_comment(comment, comment_body):
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')

    comment.reply(comment_body)
