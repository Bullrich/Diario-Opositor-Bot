import firebase_login

search_query = 'comments'
from behavior.database import verbose


def get_firebase():
    firebase = firebase_login.get_firebase()

    db = firebase_login.get_database(firebase)
    user = firebase_login.get_logged_user(firebase)
    return [user, db]


def add_id(comment_file):
    firebase = get_firebase()

    firebase[1].child(search_query).child(comment_file['comment_id']).set(comment_file, firebase[0]['idToken'])


def get_id(comment_id):
    firebase = get_firebase()

    searched_id = firebase[1].child(search_query).child(comment_id).get(firebase[0]['idToken']).val()

    return searched_id


def get_all():
    firebase = get_firebase()

    all_comments = firebase[1].child(search_query).get(firebase[0]['idToken']).val()

    all_comments_id = []

    for comment_id in all_comments:
        all_comments_id.append(comment_id)
    if verbose:
        print all_comments_id
    return all_comments_id
