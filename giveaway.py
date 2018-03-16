import praw
import argparse
import webbrowser
import time
import random

min_karma = 100
min_age_days = 60

parser = argparse.ArgumentParser(description='Client ID, private key and post link')
parser.add_argument('client_id')
parser.add_argument('key')
parser.add_argument('post')
parser.add_argument('n')
args = parser.parse_args()

r = praw.Reddit(client_id=args.client_id,
                client_secret=args.key,
                user_agent='Giveaway script for /r/flashlight by /u/Zak')

submission = r.submission(id=args.post)

comments = submission.comments
comments.replace_more(limit=512) # destructive and returns something useless

def process_comments(comments):
    now = time.mktime(time.gmtime())
    min_age = min_age_days * 24 * 60 * 60
    entrants = set()
    for c in comments:
        valid_entry = True
        if "not in" in c.body.lower():
            valid_entry = False
        if now - c.author.created_utc < min_age:
            valid_entry = False
        if c.author.comment_karma < min_karma:
            valid_entry = False
        if valid_entry:
            entrants.add(c.author)
    print len(entrants), " entries"
    print random.sample(list(entrants), int(args.n))

process_comments(comments)
