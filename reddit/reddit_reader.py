# coding=utf-8
import os
import time

import reddit_commenter
from database import firebase_crud
from reddit import bot_login
from rss import rss_search


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def get_user_comment(r, username):
    user = r.redditor(username)
    headers = []
    print "Getting comments from /u/" + user.name
    for i, u_comment in enumerate(user.comments.new()):
        append_text = find_between(u_comment.body, "[", "]")
        if " " in append_text:
            headers.append(u_comment)
            # How many commentaries
            if i > 40:
                break
    return reversed(headers)


def minutes(amount_of_minutes):
    return 60 * amount_of_minutes


def comment_and_save(comment, comment_body):
    try:
        reddit_commenter.reply_to_comment(comment, comment_body)
        # Taking some time to check if everything went accordingly
        time.sleep(10)

        comment_file = {'comment_id': comment.id, 'comment_url': 'www.reddit.com' + comment.permalink()}
        firebase_crud.add_id(comment_file)
        # If everything was successful, wait for ten minutes
        print "Successfully commented. Taking a break."
        time.sleep(minutes(10))

    except Exception, e:
        print e
        # Wait for a minute and try again
        time.sleep(minutes(1))


def format_comment(news):
    header = "## Noticias similares de otros diarios:\n\n"
    noticias_relacionadas = ''
    for new in news:
        noticias_relacionadas += ' - Diario ' + new[0] + ': '
        noticias_relacionadas += '[' + new[1]['text'].split('\n', 1)[0] + ']'
        noticias_relacionadas += '(' + new[1]['link'] + ')\n\n'
    return header + noticias_relacionadas + footer()


signature = os.environ.get('bot_firma') if os.environ.get('bot_firma') is not None else ""


def footer():
    bot_signature = "Diario Opositor Bot, distintas perspectivas de la misma noticia"
    link_al_source = "\n\n[Codigo fuente](https://github.com/Bullrich/Diario-Opositor-Bot). "

    return '---\n\n' + bot_signature + link_al_source + '\n\n' + signature


not_allowed_ends = ".jpg"


def start_reading_process(repeat):
    user_comments = get_user_comment(bot_login.bot_login(), u"empleadoEstatalBot")

    if user_comments:
        old_comments = firebase_crud.get_all()
        for comment in user_comments:
            if comment and comment.id not in old_comments:
                parsed_comment = find_between(comment.body, "[", "]")

                print "Searching for comment: " + parsed_comment
                print "Comment id: " + comment.id

                if not parsed_comment.endswith(not_allowed_ends):
                    news = rss_search.get_articles(parsed_comment)
                    if news:
                        print "\n\n--- original new: " + parsed_comment
                        formatted_comment = format_comment(news)
                        print formatted_comment
                        print '\n'

                        comment_and_save(comment, formatted_comment)
                    else:
                        print "\n\n--- No news in this platform\n\n"
        print "Finished a round. Taking a break before starting again."
        time.sleep(minutes(30))
        if repeat:
            print "Finished the loop. Starting again."
            start_reading_process()
        else:
            print "Finished the process"
