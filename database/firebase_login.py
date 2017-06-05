import os

import pyrebase


def get_firebase():
    firebase_credentials = get_credentails()
    config = {
        "apiKey": firebase_credentials[0],
        "authDomain": firebase_credentials[1],
        "databaseURL": firebase_credentials[2],
        "storageBucket": firebase_credentials[3],
        "serviceAccount": firebase_credentials[4],
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


def get_credentails():
    if os.environ.get('FIREBASE_APIKEY'):
        firebase_login = [os.environ['FIREBASE_APIKEY'],
                          os.environ['FIREBASE_AUTHDOMAIN'],
                          os.environ['FIREBASE_DB_URL'],
                          os.environ['FIREBASE_STORAGE'],
                          os.environ['FIREBASE_SERVICE']]
    else:
        from configs import credentials
        firebase_login = [credentials.firebase_config.apikey,
                          credentials.firebase_config.auth_domain,
                          credentials.firebase_config.database_url,
                          credentials.firebase_config.storage_bucket,
                          credentials.firebase_config.service_account]
    return firebase_login


def get_user_login():
    from configs import credentials
    if os.environ.get('FIREBASE_USER'):
        user_credentials = [os.environ['FIREBASE_USER'],
                            os.environ['FIREBASE_PASS']]
    else:
        user_credentials = [credentials.firebase_config.user_email,
                            credentials.firebase_config.user_pass]

    return user_credentials
