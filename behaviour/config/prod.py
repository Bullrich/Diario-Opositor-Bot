import os


def get_credentials():
    return {
        'reddit': {
            'username': os.environ['REDDIT_USERNAME'],
            'password': os.environ['REDDIT_PASSWORD'],
            'client_id': os.environ['REDDIT_CLIENT_ID'],
            'client_secret': os.environ['REDDIT_CLIENT_SECRET']
        },
        'firebase': {
            'apikey': os.environ['FIREBASE_API_KEY'],
            'auth_domain': os.environ['FIREBASE_AUTH_DOMAIN'],
            'database_url': os.environ['FIREBASE_DATABASE_URL'],
            'storage_bucket': os.environ['FIREBASE_STORAGE_BUCKET'],
            'service_account': os.environ['FIREBASE_SERVICE_ACOUNT'],
            'user_email': os.environ['FIREBASE_USER_EMAIL'],
            'user_pass': os.environ['FIREBASE_USER_PASS']
        }
    }
