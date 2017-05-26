import os

import praw


def bot_login():
    print "Logging in.."
    login_credential = retrieve_login_credentials()
    print login_credential
    r_authentication = praw.Reddit(username=login_credential[0],
                                   password=login_credential[1],
                                   client_id=login_credential[2],
                                   client_secret=login_credential[3],
                                   user_agent="DogTest on commenting with jokes v.01 ")
    print "Logged in!"
    return r_authentication


def retrieve_login_credentials():
    if os.environ.get('REDDIT_USERNAME', None):
        login_info = [os.environ['REDDIT_USERNAME'],
                      os.environ['REDDIT_PASSWORD'],
                      os.environ['REDDIT_CLIENT_ID'],
                      os.environ['REDDIT_CLIENT_SECRET']]
    else:
        from configs import credentials
        login_info = [credentials.username,
                      credentials.password,
                      credentials.client_id,
                      credentials.client_secret]
    return login_info
