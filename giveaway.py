import praw
import argparse
import webbrowser
import time

min_karma = 100
min_age_days = 60

parser = argparse.ArgumentParser(description='Client ID, private key and post link')
parser.add_argument('client_id')
parser.add_argument('key')
parser.add_argument('post')
args = parser.parse_args()

r = praw.Reddit('Giveaway script for /r/flashlight by /u/Zak')

r.set_oauth_app_info(client_id=args.client_id,
                     client_secret=args.key,
                     redirect_uri='http://127.0.0.1:65010/authorize_callback')

url = r.get_authorize_url('uniqueKey', 'submit', True)
webbrowser.open(url)

access_code = raw_input('Enter access code: ')

access_information = r.get_access_information(access_code)

r.set_access_credentials(**access_information)

submission = r.get_submission(submission_id=args.post)
submission.replace_more_comments(limit=None, threshold=0)
comments = submission.comments

def process_comments(comments):
    n = 1
    now = time.mktime(time.gmtime())
    min_age = min_age_days * 24 * 60 * 60
    for c in comments:
        reply = ""
        if "not in" in c.body.lower():
            reply = reply + "\"Not in\" detected in comment: your non-participation is acknowledged\n\n"
        if now - c.author.created_utc < min_age:
            reply = reply + "Your account is not old enough to participate: {min_age_days} days is the minimum\n\n".format(min_age_days=min_age_days, **locals())
        if c.author.comment_karma < min_karma:
            reply = reply + "Your comment karma ({c.author.comment_karma}) is below the minimum ({min_karma}) - please participate constructively on reddit to earn more karma and try again in the next giveaway\n\n".format(min_karma=min_karma, **locals())
        if len(reply) == 0:
            reply = str(n)
            n = n+1
        c.reply(reply)
    print n, " entries"

process_comments(comments)