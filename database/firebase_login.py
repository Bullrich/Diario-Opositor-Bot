import pyrebase

from configs import credentials


def get_firebase():
    config = {
        "apiKey": credentials.firebase_config.apikey,
        "authDomain": credentials.firebase_config.auth_domain,
        "databaseURL": credentials.firebase_config.database_url,
        "storageBucket": credentials.firebase_config.storage_bucket,
        "serviceAccount": credentials.firebase_config.service_account
    }
    firebase = pyrebase.initialize_app(config)

    return firebase


def get_database(firebase):
    db = firebase.database()
    return db


def get_logged_user(firebase):
    firebase = get_firebase()

    auth = firebase.auth()
    # authenticate a user
    user = auth.sign_in_with_email_and_password(credentials.firebase_config.user_email,
                                                credentials.firebase_config.user_pass)

    return user
