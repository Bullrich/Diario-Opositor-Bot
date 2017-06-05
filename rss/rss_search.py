# coding=utf-8
"""
news.py: an rss feed aggregator/filter
"""
import difflib
from operator import or_
from re import search
from urllib import urlretrieve

from feedparser import parse

LIM = 3


def get_list_from_string(s):
    """ returns a list of lines """
    return s.strip().splitlines()


def get_text_from_feed_entry(entry):
    """ returns a dict from entry containing text and link """
    return {'text': entry.title + '\n' + entry.summary, 'link': entry.link}


def matches_word(text, word):
    """ checks if text matches word """
    if search(r'\b' + word.lower() + r'\b', text.lower()):
        return True
    else:
        return False


def matches_any_word(text, keywords):
    """ checks if text matches any of the keywords """
    return reduce(or_, [matches_word(text, word) for word in keywords])


def rss_search(urls, keywords):
    """ main function """
    raw_data_list = [parse(url) for url in urls]
    entries = sum([raw_data.entries for raw_data in raw_data_list], [])

    required_data = [get_text_from_feed_entry(entry) for entry in entries]

    print 'searching {} entries...'.format(len(required_data))
    results = filter(
        lambda data: matches_any_word(data['text'], keywords),
        required_data
    )

    if results:

        result_count = len(results)
        short_result = []
        print '{} result(s) found'.format(result_count)

        for i, result in enumerate(results):
            if debug_news:
                print 'downloading {} of {}...'.format(i + 1, result_count),
                urlretrieve(result['link'])  # , filename)
                print 'done'
            short_result.append(result)
        return results
    else:
        print 'no results found'
        print 'try again with more keywords and urls'
        return None


def get_urls():
    from configs import urls
    _urls = urls.rss
    return _urls


def get_key_words(title):
    from configs import filteredWords
    common_words = filteredWords.filtered
    title_words = title.lower().split()
    # keywords = set(title_words).difference(common_words)
    keywords = [item for item in title_words if item not in common_words]
    return keywords


debug_news = None


# This functions checks, given a news article title, for the most similar news in a couple of rss links.
# The idea is to find the same story from a different newspaper
def get_articles(article_text):
    rss_feed = []
    rss_urls = get_urls()
    # Get the key words from the article text
    article_key_words = get_key_words(article_text)

    for key in rss_urls:

        try:
            print "Getting from " + key
            # Get rss feed with related urls
            results = rss_search(rss_urls[key], article_key_words)  # Json with two fields, [link] and [text]
            # Create the list that will contain only the test news
            text_news = []

            if results:
                for news in results:
                    # Add the [text] value to a new list
                    text_news.append(news['text'])
                # finds inside the list related news to one that is closest to the reference one
                if debug_news:
                    print "text_news length: " + str(len(text_news))

                # Declare a list to contain only the headers
                news_header = []
                for news in text_news:
                    news_header.append(news.split('\n', 1)[0])
                if debug_news:
                    print news_header

                # Get the closest matches from the matches, with a max error of the cutoff value
                # increase that to be more precise
                closest_news = difflib.get_close_matches(" ".join(article_key_words), news_header, n=4, cutoff=0.46)

                if debug_news:
                    print " -- closest news"
                    print closest_news

                from difflib import SequenceMatcher
                if closest_news:
                    compare_news = closest_news[0].split('\n', 1)[0]
                    if debug_news:
                        print compare_news

                    # We check that the title isn't exactly the same to filter out the same news
                    if SequenceMatcher(a=compare_news, b=article_text).ratio() < 0.9:

                        if debug_news:
                            print "Sequence error: "
                            print SequenceMatcher(a=compare_news, b=article_text).ratio()

                        if debug_news:
                            print " -- text news"
                            print text_news

                        # Find what is the index of the list
                        list_index = news_header.index(closest_news[0])
                        if debug_news:
                            print text_news[list_index].split('\n', 1)[0]
                            print list_index
                        # Return that element (the most similar one)
                        rss_feed.append([key, results[list_index]])
        except Exception, e:
            print "Failed with site: " + key
            print "Failed with the following exception:"
            print e

    return rss_feed
