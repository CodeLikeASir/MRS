import pandas as pd
import praw
import json
import time
import datetime
import configparser
import argparse, sys
from praw.models.listing.mixins import subreddit

def checkDate(first, last, date):
    print("Checking date")
    return date > first and date < last

def intToDate(value):
    return datetime.datetime.utcfromtimestamp(value).strftime('%Y-%m-%d')

def dateToInt(date):
    return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())


parser=argparse.ArgumentParser()

parser.add_argument('--fileName', help='Change the generated file name', default='scrap')
parser.add_argument('--subr', help='Name of subreddit to search in', default='all')
parser.add_argument('--mode', help='Modes to filter (more info in readme)', default=0)
parser.add_argument('--keyword', help='Keyword to search for', default='_')
parser.add_argument('--start', help='First date to find results for, format YYYY-MM-DD, example: 2020-01-01', default=0)
parser.add_argument('--end', help='Last date to find results for', default=0)
parser.add_argument('--nrPosts', help='Number of posts to analyze', default=100)

args=parser.parse_args()

subreddit = args.subr
mode = args.mode
keyword = args.keyword

if not args.start == 0:
    start = dateToInt(args.start)
else:
    start = args.start

if not args.end == 0:
    end = dateToInt(args.end)
else:
    end = args.end
    
analyzedPosts = args.nrPosts

configParser = configparser.RawConfigParser()   
configFilePath = r'config.txt'
configParser.read(configFilePath)

reddit = praw.Reddit(client_id=configParser.get('api-key', 'client_id'), 
                    client_secret=configParser.get('api-key', 'client_secret'), 
                    user_agent=configParser.get('api-key', 'user_agent'))

posts = []
print("Starting to look for " + keyword + " in " + subreddit)
if(start > 0 and end > 0):
    print("From " + intToDate(start) + " to " + intToDate(end))

if keyword == "_":
    for post in reddit.subreddit(subreddit).top(limit=int(analyzedPosts)):
        posts.append([post.title, post.score, post.subreddit, post.num_comments, intToDate(post.created_utc)])
elif mode == 0:
    for post in reddit.subreddit(subreddit).top(limit=int(analyzedPosts)):
        if(post.link_flair_text == keyword):
            if(start == 0 or checkDate(start, end, post.created_utc)):
                posts.append([post.title, post.score, post.subreddit, post.num_comments, intToDate(post.created_utc)])
elif mode == 1:
    for post in reddit.subreddit(subreddit).top(limit=int(analyzedPosts)):
        if(keyword in post.title):
            if(start == 0 or checkDate(start, end, post.created_utc)):
                posts.append([post.title, post.score, post.subreddit, post.num_comments, intToDate(post.created_utc)])

print("Found " + str(len(posts)) + " results.")   
posts = pd.DataFrame(posts,columns=['title', 'score', 'subreddit', 'num_comments', 'created'])
    
posts.to_csv(args.fileName + ".csv", index=False)