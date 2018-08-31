import logging

import pyrebase


class FirebaseController:
    def __init__(self, credentials):
        self.logger = logging.getLogger(__name__)
        config = {
            "apiKey": credentials['apikey'],
            "authDomain": credentials['auth_domain'],
            "databaseURL": credentials['database_url'],
            "storageBucket": credentials['storage_bucket']
        }
        self.logger.info('Logging into Firebase')
        firebase = pyrebase.initialize_app(config)
        self.database = firebase.database()
        self.user = firebase.auth().sign_in_with_email_and_password(credentials['user_email'], credentials['user_pass'])
        self.logger.info('Logged in!')
        self.search_query = 'comments'

    def add_comment(self, comment_file):
        self.database.child(self.search_query). \
            child(comment_file['comment_id']). \
            set(comment_file, self.user['idToken'])
        self.logger.info("'Added' to the database")

    def fake_db_to_txt_file(self, comment_file):
        f = open("comments.txt", "a+")
        f.write(comment_file['comment_url'] + '\n')
        f.close()

    def get_id(self, comment_id):
        searched_id = self.database.child(self.search_query).child(comment_id).get(self.user['idToken']).val()
        return searched_id

    def get_all_comments(self):
        all_comments = self.database.child(self.search_query).get(self.user['idToken']).val()

        all_comments_id = []

        for comment_id in all_comments:
            all_comments_id.append(comment_id)

        self.logger.debug(all_comments_id)
        return all_comments_id
