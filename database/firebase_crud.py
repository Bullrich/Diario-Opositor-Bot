import firebase_login

search_query = 'comments'

def add_id(comment_id):
    firebase = firebase_login.get_firebase()

    db = firebase_login.get_database(firebase)
    user = firebase_login.get_logged_user(firebase)

    new_id = {'comment_id': comment_id}
    db.child(search_query).child(comment_id).set(new_id, user['idToken'])


def get_id(comment_id):
    firebase = firebase_login.get_firebase()

    db = firebase_login.get_database(firebase)
    user = firebase_login.get_logged_user(firebase)

    searched_id = db.child(search_query).child(comment_id).get(user['idToken']).val()

    return searched_id

def get_all():
    firebase = firebase_login.get_firebase()

    db = firebase_login.get_database(firebase)
    user = firebase_login.get_logged_user(firebase)

    all_comments=db.child(search_query).get(user['idToken']).val()

    all_comments_id=[]

    for cmmt_id in all_comments:
        all_comments_id.append(cmmt_id)

    return all_comments_id