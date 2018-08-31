# coding=utf-8
"""
news.py: an rss feed aggregator/filter
"""
import difflib
from functools import reduce
from operator import or_
from re import search

import requests
from feedparser import parse

from behavior.StatusReporter import Status


class RssSearcher:
    def __init__(self, urls, filtered_words, status_reporter):
        import logging
        self.logger = logging.getLogger(__name__)
        self.urls = urls
        self.filtered_words = filtered_words
        self.status = status_reporter
        self.raw_data = {}

    def get_list_from_string(self, s):
        """ returns a list of lines """
        return s.strip().splitlines()

    def get_text_from_feed_entry(self, entry):
        """ returns a dict from entry containing text and link """
        return {'text': entry.title + '\n' + entry.summary, 'link': entry.link}

    def matches_word(self, text, word):
        """ checks if text matches word """
        try:
            if search(r'\b' + word.lower() + r'\b', text.lower()):
                return True
        except Exception as e:
            self.logger.error(e)
        return False

    def matches_any_word(self, text, keywords):
        """ checks if text matches any of the keywords """
        return reduce(or_, [self.matches_word(text, word) for word in keywords])

    def workaround_parse(self, url):
        p = parse(url)
        if not p['entries'] and "not well-formed" in str(p['bozo_exception']):
            rss1 = requests.get(url).content.decode("utf-8")
            rss1 = rss1.replace("utf-8", "unicode")
            p = parse(rss1)
        return p['entries']

    def cached_raw_data_list(self, site, url):
        if site not in self.raw_data:
            self.status.update_status(Status.GETTING_ARTICLES)
            print(site + ' / ' + str(url) + ' is not in raw data cache!')
            self.raw_data[site] = self.workaround_parse(url)
        return self.raw_data[site]

    # TODO: make the rss searcher store all the src instead of re downloading them all the time
    def rss_search(self, key, urls, keywords):
        """ main function """
        raw_data_list = [self.cached_raw_data_list(key, url) for url in urls]

        entries = sum([raw_data for raw_data in raw_data_list], [])

        required_data = [self.get_text_from_feed_entry(entry) for entry in entries]

        self.logger.debug('searching {} entries...'.format(len(required_data)))
        results = list(filter(lambda data: self.matches_any_word(data['text'], keywords), required_data))

        if results:
            result_count = len(results)
            short_result = []
            self.logger.debug('{} result(s) found'.format(result_count))

            for i, result in enumerate(results):
                # print('downloading {} of {}...'.format(i + 1, result_count), urlretrieve(result['link']))
                self.logger.debug('%s done', key)
                short_result.append(result)
            return results
        else:
            self.logger.debug('no results found')
            self.logger.debug('try again with more keywords and urls')
            return None

    def get_key_words(self, title):
        title_words = title.lower().split()
        # keywords = set(title_words).difference(common_words)
        keywords = [item for item in title_words if item not in self.filtered_words]
        return keywords

    # This functions checks, given a news article title, for the most similar news in a couple of rss links.
    # The idea is to find the same story from a different newspaper
    def get_articles(self, article_text, similarity=0.52):
        rss_feed = []
        # Get the key words from the article text
        article_key_words = self.get_key_words(article_text)

        for key in self.urls:

            try:
                self.logger.info("Getting from " + key)
                # Get rss feed with related urls
                results = self.rss_search(key, self.urls[key],
                                          article_key_words)  # Json with two fields, [link] and [text]
                # Create the list that will contain only the test news
                text_news = []

                if results:
                    for news in results:
                        # Add the [text] value to a new list
                        text_news.append(news['text'])
                        # finds inside the list related news to one that is closest to the reference one
                        # self.logger.debug("text_news length: " + str(len(text_news)))

                    # Declare a list to contain only the headers
                    news_header = []
                    for news in text_news:
                        news_header.append(news.split('\n', 1)[0])
                    self.logger.debug(news_header)

                    # Get the closest matches from the matches, with a max error of the cutoff value
                    # increase that to be more precise
                    closest_news = difflib.get_close_matches(" ".join(article_key_words), news_header, n=4,
                                                             cutoff=similarity)

                    self.logger.debug(" -- closest news")
                    self.logger.debug(closest_news)

                    from difflib import SequenceMatcher
                    if closest_news:
                        compare_news = closest_news[0].split('\n', 1)[0]
                        self.logger.debug(compare_news)

                        # We check that the title isn't exactly the same to filter out the same news
                        if SequenceMatcher(a=compare_news, b=article_text).ratio() < 0.9:
                            self.logger.debug("Sequence error: ")
                            self.logger.debug(SequenceMatcher(a=compare_news, b=article_text).ratio())

                            self.logger.debug(" -- text news")
                            self.logger.debug(text_news)

                            # Find what is the index of the list
                            list_index = news_header.index(closest_news[0])

                            self.logger.debug(text_news[list_index].split('\n', 1)[0])
                            self.logger.debug(list_index)
                            # Return that element (the most similar one)
                            rss_feed.append([key, results[list_index]])
            except Exception as e:
                self.logger.warning("Failed with site: " + key)
                self.logger.warning("Failed with the following exception:")
                self.logger.debug(e)

        return rss_feed
