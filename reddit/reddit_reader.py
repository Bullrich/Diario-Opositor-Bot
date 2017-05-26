# coding=utf-8
import time

import reddit_commenter
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
            # How many comentaries
            if i > 15:
                break
    return headers


def comment_and_save(comment, comment_body):
    print id
    try:
        reddit_commenter.reply_to_comment(comment, comment_body)
        # Taking some time to check if everything went accordly
        time.sleep(10)
        reddit_commenter.save_comment_id_to_file(comment.id)
        # If everything was successfull, wait for ten minutes
        time.sleep(600)

    except Exception, e:
        print e
        # Wait for a minute and try again
        time.sleep(60)


def format_comment(news):
    header = "## Noticias similares de otros diarios:\n\n"
    noticias_relacionadas = ''
    for new in news:
        noticias_relacionadas += ' - Diario ' + new[0] + ': '
        noticias_relacionadas += '[' + new[1]['text'].split('\n', 1)[0] + ']'
        noticias_relacionadas += '(' + new[1]['link'] + ')\n\n'
    footer = "---\n\nDiario Opositor Bot, distintas perspectivas de la misma noticia"
    return header + noticias_relacionadas + footer


not_allowed_ends = ".jpg"


def start_reading_process():
    user_comments = get_user_comment(bot_login.bot_login(), u"empleadoEstatalBot")

    if user_comments:
        old_comments = reddit_commenter.get_saved_comments()
        for comment in user_comments:
            if comment and comment.id not in old_comments:
                parsed_comment = find_between(comment.body, "[", "]")

                print "Searching for comment: " + parsed_comment
                print "Comment id: " + comment.id

                if not parsed_comment.endswith(not_allowed_ends):
                    news = rss_search.get_articles(parsed_comment)
                    if news:
                        print "--- original new: " + parsed_comment
                        formatted_comment = format_comment(news)
                        print formatted_comment
                        print '\n'

                        comment_and_save(comment, formatted_comment)
                        # for new in news:
                        #   print "--- " + new[0] + ": " + new[1]['text'].split('\n', 1)[0]
                    else:
                        print "--- No news in this platform"
