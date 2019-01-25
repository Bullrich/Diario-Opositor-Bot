import logging

from . import Status


class StatusReporter:
    def __init__(self, safe_dict=None):
        self.logger = logging.getLogger(__name__)

        if safe_dict is not None:
            with safe_dict as status_dict:
                status_dict['status'] = {}
        else:
            self.logger.error('No dictionary available!')
        self.communication_dict = safe_dict

        self.update_status(Status.INITIALIZING)
        self.report = []

    def can_report_status(self):
        if 'status' in self.communication_dict:
            return True
        return False

    def update_status(self, status, extra_data=None):
        if self.can_report_status():
            status = {'status': status.value, 'data': extra_data}
            with self.communication_dict as comm_dict:
                comm_dict['status'] = status

    def save_report(self, comment_id, sources):
        self.report.append([comment_id, sources])

    def get_status(self):
        if self.can_report_status():
            return self.communication_dict['status']

    def clear_status(self):
        if self.can_report_status():
            with self.communication_dict as comm_dict:
                comm_dict['status'] = {}
