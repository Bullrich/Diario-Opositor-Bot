import logging
from json import dumps

import redis

from . import Status


class StatusReporter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.r = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)
        self.redis_available = self.is_redis_available()
        self.status = {}
        self.update_status(Status.INITIALIZING)

    def update_status(self, status, extra_data=None):
        self.status = {'status': status.value, 'data': extra_data}
        if self.redis_available:
            self.r.set('dob-status', dumps(self.status))

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