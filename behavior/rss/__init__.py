# coding=utf-8
import logging


def generate_urls(url_data):
    logger = logging.getLogger(__name__)
    rss = url_data['rss']
    newspapers = {}
    for newspaper in rss:
        urls_list = url_data[newspaper]['urls']
        newspapers[url_data[newspaper]["name"]] = encode_list(urls_list)
        logger.debug(newspapers)
    return newspapers


def encode_list(list):
    return [x.encode('utf-8') for x in list]
