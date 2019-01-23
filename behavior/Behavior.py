import logging
import time

import yaml

from behavior.config import fetch_credentials
from . import utils
from .StatusReporter import StatusReporter, Status
from .commenter import Commenter
from .database import FirebaseController
from .reddit import RedditController
from .rss import RssSearcher, generate_urls, encode_list


class Behavior:
    def __init__(self, signature='', pause=1, redis_url='0.0.0.0'):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing behavior")
        credentials = fetch_credentials()
        self.reddit = RedditController.RedditController(credentials['reddit'])
        self.database = FirebaseController.FirebaseController(credentials['firebase'])
        self.commenter = Commenter.Commenter(signature)
        self.status = StatusReporter.StatusReporter(redis_url)
        self.rss = self.create_rss_searcher()
        self.pause = pause

    def get_yml_file(self, yml_file_name):
        yml_file = open(yml_file_name)
        yml_data = yaml.safe_load(yml_file)
        yml_file.close()
        self.logger.debug(yml_file_name)
        self.logger.debug(yml_data)
        return yml_data

    def create_rss_searcher(self):
        urls = self.get_yml_file("config/urls.yml")
        urls = generate_urls(urls)
        filtered_words = encode_list(self.get_yml_file("config/filtered_words.yml")['filtered_words'])
        return RssSearcher.RssSearcher(urls, filtered_words, self.status)

    def read_and_respond(self):
        self.status.update_status(Status.INITIALIZING)
        comments_to_answer = self.fetch_and_format_comments(u'empleadoEstatalBot', ['argentina', 'RepublicaArgentina'])
        self.manage_commenting(comments_to_answer)
        self.status.update_status(Status.OFF)

    def manage_commenting(self, comments):
        for comment in comments:
            self.status.update_status(Status.COMMENTING, comment.to_dict())
            response = self.reddit.reply_to_comment(comment)
            comment.reply_link = response.permalink
            self.status.update_status(Status.UPDATING_DB, comment.to_dict())
            self.database.add_comment(comment)
            self.logger.info('Successfully commented! Taking a break for %i minutes', self.pause)
            self.status.update_status(Status.RESTING)
            time.sleep(utils.minutes(self.pause))

    def fetch_and_format_comments(self, username, subreddits):
        comments_to_fetch = 180
        user_comments = self.reddit.get_user_comments(username, comments_to_fetch)
        self.status.update_status(Status.FETCHING_COMMENTS_FROM_USER, {'comments': comments_to_fetch})

        if user_comments:
            self.status.update_status(Status.FETCHING_COMMENTS_FROM_DB)
            old_comments = self.database.get_all_comments()
            if old_comments:
                comments = list(filter(lambda c: c.id not in old_comments and c.subreddit in subreddits, user_comments))
            else:
                comments = user_comments
            parsed_comments = list(map(self.generate_reply_object, comments))
            return list(filter(None, parsed_comments))
        return []

    def get_related_news(self, comment):
        self.logger.info('------ Searching for comment: %s', comment)
        news = self.rss.get_articles(comment, similarity=0.6)
        if news:
            return news
        else:
            self.logger.warning('No related news')
            return []

    def generate_reply_object(self, comment):
        self.status.update_status(Status.FINDING_RELATED_NEWS, comment.id)
        comment_text = utils.find_between(comment.body, '[', ']')
        related_news = self.get_related_news(comment_text)
        if related_news:
            reply = self.commenter.format_comment(related_news)
            self.logger.info(reply)
            return self.Comment(comment, reply)
        else:
            return None

    class Comment:
        def __init__(self, comment, reply):
            self.comment = comment
            self.message = utils.find_between(comment.body, '[', ']')
            self.id = comment.id
            self.link = 'reddit.com' + comment.permalink
            self.reply = reply
            self.reply_link = ''

        def to_dict(self):
            return {'id': self.id, 'message': self.message, 'link': self.link,
                    'reply_link': 'reddit.com' + self.reply_link}
