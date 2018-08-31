import praw
import logging


class RedditController:
    def __init__(self, credentials):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Reddit Controller initiated")
        self.r = self.login(credentials)

    def login(self, credentials):
        self.logger.info("Logging in...")
        r = praw.Reddit(username=credentials['username'],
                        password=credentials['password'],
                        client_id=credentials['client_id'],
                        client_secret=credentials['client_secret'],
                        user_agent="Diario Opositor Bot")
        return r

    def reply_to_comment(self, comment, reply_body):
        comment.reply(reply_body)
        self.logger.info("'Commented'")

    def get_user_comments(self, username, comments_to_fetch=100):
        user = self.r.redditor(username)
        headers = []
        self.logger.info("Getting comments from /u/" + user.name)
        for i, u_comment in enumerate(user.comments.new()):
            append_text = find_between(u_comment.body, "[", "]")
            if " " in append_text:
                headers.append(u_comment)
                # How many commentaries
                if i > comments_to_fetch:
                    break
        return reversed(headers)


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""
