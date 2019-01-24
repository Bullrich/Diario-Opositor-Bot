import logging
from json import dumps

import redis

from . import Status


class StatusReporter:
    def __init__(self, redis_url='0.0.0.0'):
        self.logger = logging.getLogger(__name__)
        self.r = redis.StrictRedis(host=redis_url, port=6379, db=0)
        self.redis_available = self.is_redis_available()
        self.status = {}
        self.update_status(Status.INITIALIZING)
        self.report = []

    def update_status(self, status, extra_data=None):
        self.status = {'status': status.value, 'data': extra_data}
        if self.redis_available:
            self.r.set('dob-status', dumps(self.status))

    def save_report(self, comment_id, sources):
        self.report.append([comment_id, sources])

    def get_status(self):
        return self.status

    def is_redis_available(self):
        try:
            # getting None returns None or throws an exception
            self.r.get(None)
        except (redis.exceptions.ConnectionError,
                redis.exceptions.BusyLoadingError):
            return False
        return True

    def clear_status(self):
        if self.redis_available:
            self.r.delete('dob-status')
