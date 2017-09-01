# coding=utf-8
import time

import behavior
import reddit_commenter
from behavior.commenter import comment_formatter
from behavior.reddit import bot_login


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
    limit = 70
    for i, u_comment in enumerate(user.comments.new()):
        append_text = find_between(u_comment.body, "[", "]")
        if " " in append_text:
            headers.append(u_comment)
            # How many commentaries
            if i > limit:
                break
    return reversed(headers)


def minutes(amount_of_minutes):
    return 60 * amount_of_minutes


def comment_and_save(comment, comment_body):
    try:
        reddit_commenter.reply_to_comment(comment, comment_body)
        # Taking some time to check if everything went accordingly
        time.sleep(5)

        comment_file = {'comment_id': comment.id, 'comment_url': 'www.reddit.com' + comment.permalink()}
        behavior.add_comment_id(comment_file)
        # If everything was successful, wait before iterating again
        print "Successfully commented. Taking a break."
        time.sleep(minutes(5))

    except Exception, e:
        print e
        # Wait for a minute and try again
        time.sleep(minutes(1))


def start_reading_process(repeat, username, subreddit):
    user_comments = get_user_comment(bot_login.bot_login(), username)

    if user_comments:
        old_comments = behavior.get_all_comments()
        for comment in user_comments:
            if comment and comment.id not in old_comments and comment.subreddit == subreddit:
                parsed_comment = find_between(comment.body, "[", "]")

                print "\nSearching for comment: " + parsed_comment

                news = behavior.get_articles(parsed_comment)
                if news:
                    print "\n\n--- original new: " + parsed_comment
                    formatted_comment = comment_formatter.format_comment(news)
                    print formatted_comment
                    print '\n\n'

                    comment_and_save(comment, formatted_comment)
                else:
                    print "\n\n--- No news in this platform\n\n"

    if repeat:
        print "Finished a round. Taking a break before starting again."
        time.sleep(minutes(30))
        print "Finished the loop. Starting again."
        start_reading_process(repeat)
    else:
        print "Finished the process"
