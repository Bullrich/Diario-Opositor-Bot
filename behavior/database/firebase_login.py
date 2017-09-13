import pyrebase
import yaml


def get_firebase():
    firebase_credentials = get_credentials()
    config = {
        "apiKey": firebase_credentials[0],
        "authDomain": firebase_credentials[1],
        "databaseURL": firebase_credentials[2],
        "storageBucket": firebase_credentials[3]
    }
    firebase = pyrebase.initialize_app(config)

    return firebase


def get_database(firebase):
    db = firebase.database()
    return db


def get_logged_user(firebase):
    auth = firebase.auth()
    user_credentials = get_user_login()
    # authenticate a user
    user = auth.sign_in_with_email_and_password(user_credentials[0],
                                                user_credentials[1])

    return user


def get_credentials():
    firebase_credentials = retrieve_credentials()
    firebase_login = [firebase_credentials['apikey'],
                      firebase_credentials['auth_domain'],
                      firebase_credentials['database_url'],
                      firebase_credentials['storage_bucket']]
    return firebase_login


def retrieve_credentials():
    credentials = open("credentials.yml")
    credentials_data = yaml.safe_load(credentials)
    credentials.close()
    return credentials_data['firebase']


def get_user_login():
    firebase_credentials = retrieve_credentials()
    user_credentials = [firebase_credentials['user_email'],
                        firebase_credentials['user_pass']]

    return user_credentials
