import yaml
from .reddit import RedditController
from .database import FirebaseController
from .commenter import Commenter
from .rss import RssSearcher, generate_urls, encode_list
from .StatusReporter import StatusReporter, Status
from . import utils
import time
import logging


class Behavior:
    def __init__(self, signature='', pause=1, redis_url='0.0.0.0'):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing behavior")
        credentials = self.get_yml_file('credentials.yml')
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
        self.comment_replies(comments_to_answer)
        self.status.update_status(Status.OFF)

    def fetch_and_format_comments(self, username, subreddits):
        comments_to_fetch = 180
        user_comments = self.reddit.get_user_comments(username, comments_to_fetch)
        self.status.update_status(Status.FETCHING_COMMENTS_FROM_USER, {'comments': comments_to_fetch})

        if user_comments:
            old_comments = self.database.get_all_comments()
            self.status.update_status(Status.FETCHING_COMMENTS_FROM_DB)
            comments = list(filter(lambda c: c.id not in old_comments and c.subreddit in subreddits, user_comments))
            parsed_comments = list(map(self.get_related_news, comments))
            return list(filter(None, parsed_comments))
        return []

    def comment_replies(self, parsed_comments):
        for comment in parsed_comments:
            comment_file = {'comment_id': comment['comment'].id,
                            'comment_url': 'www.reddit.com' + comment['comment'].permalink}
            self.reddit.reply_to_comment(comment['comment'], comment['reply'])
            self.status.update_status(Status.COMMENTING, comment['comment'].id)
            self.database.add_comment(comment_file)
            self.status.update_status(Status.UPDATING_DB, comment['comment'].id)
            self.logger.info('Successfully commented!. Taking a break for %i minutes', self.pause)
            self.status.update_status(Status.RESTING)
            time.sleep(utils.minutes(self.pause))

    def get_related_news(self, comment):
        self.status.update_status(Status.FINDING_RELATED_NEWS, comment.id)
        parsed_comment = utils.find_between(comment.body, '[', ']')
        self.logger.info('------ Searching for comment: %s', parsed_comment)
        news = self.rss.get_articles(parsed_comment, similarity=0.6)
        if news:
            formatted_comment = self.commenter.format_comment(news)
            self.logger.info(formatted_comment)
            return {'comment': comment, 'reply': formatted_comment}
        else:
            self.logger.warning('No related news')
            return []
