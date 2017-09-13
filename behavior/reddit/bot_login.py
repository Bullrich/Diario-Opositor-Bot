import praw
import yaml


def bot_login():
    print "Logging in.."
    login_credential = retrieve_login_credentials()
    r_authentication = praw.Reddit(username=login_credential['username'],
                                   password=login_credential['password'],
                                   client_id=login_credential['client_id'],
                                   client_secret=login_credential['client_secret'],
                                   user_agent="Diario Opositor Bot")
    print "Logged in!"
    return r_authentication


def retrieve_login_credentials():
    credentials = open("credentials.yml")
    credentials_data = yaml.safe_load(credentials)
    credentials.close()

    reddit_credentials = credentials_data['reddit']
    return reddit_credentials
