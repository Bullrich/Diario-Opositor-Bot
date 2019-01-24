from enum import Enum


class Status(Enum):
    INITIALIZING = 'initializing'
    FETCHING_COMMENTS_FROM_USER = 'fetching_comments_from_user'
    FETCHING_COMMENTS_FROM_DB = 'fetching_comments_from_db'
    FILTERING_ANALYZED_COMMENTS = 'filtering_analyzed_comments'
    MAPPING_COMMENTS = 'mapping_comments'
    GETTING_ARTICLES = 'getting_articles'
    FINDING_RELATED_NEWS = 'finding_related_news'
    COMMENTING = 'commenting'
    UPDATING_DB = 'updating_db'
    RESTING = 'resting'
    OFF = 'off'
