import pandas as pd
import praw
import json
import time
import datetime
import configparser
import argparse, sys
from praw.models.listing.mixins import subreddit

def checkDate(first, last, date):
    return start == 0 or (date > first and date < last)

def intToDate(value):
    return datetime.datetime.utcfromtimestamp(value).strftime('%Y-%m-%d')

def dateToInt(date):
    return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple())


parser=argparse.ArgumentParser()

parser.add_argument('--subr', help='name of subreddit to search in', default='all')
parser.add_argument('--mode', help='modes to filter (more info in readme.txt)', default=0)
parser.add_argument('--keyword', help='keyword to search for', default='_')
parser.add_argument('--start', help='first date to find results for, format YYYY-MM-DD, example: 2020-01-01', default=0)
parser.add_argument('--end', help='last date to find results for', default=0)
parser.add_argument('--nrPosts', help='number of posts to analyze', default=100)
parser.add_argument('--fileName', help='change the generated file name', default='scrap')
parser.add_argument('--format', help='format of output file, can be csv or json (EXPERIMENTAL)', default='csv')

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
    
analyzedPosts = int(args.nrPosts)

configParser = configparser.RawConfigParser()   
configFilePath = r'config.txt'
configParser.read(configFilePath)

reddit = praw.Reddit(client_id=configParser.get('api-key', 'client_id'), 
                    client_secret=configParser.get('api-key', 'client_secret'), 
                    user_agent=configParser.get('api-key', 'user_agent'))

print("Starting to look for " + keyword + " in " + subreddit)
if(start > 0 and end > 0):
    print("From " + intToDate(start) + " to " + intToDate(end))

postsAnalyzed = 0
analyzedPosts = 10000
posts = []

# rework with: 

if keyword == "_":
    for post in reddit.subreddit(subreddit).top(limit=analyzedPosts):
        if(checkDate(start, end, post.created_utc)):
            posts.append([post.title, post.score, post.subreddit, post.num_comments, intToDate(post.created_utc)])
elif int(mode) == 0:
    print("entered mode 0")
    for post in reddit.subreddit(subreddit).top(limit=analyzedPosts):
        if(post.link_flair_text == keyword):
            if(checkDate(start, end, post.created_utc)):
                posts.append([post.title, post.score, post.subreddit, post.num_comments, intToDate(post.created_utc)])
elif int(mode) == 1:
    for post in reddit.subreddit(subreddit).search(keyword, sort='relevance'):
        posts.append([post.title, post.score, post.subreddit, post.num_comments, intToDate(post.created_utc)])

print("Analyzed " + str(postsAnalyzed))
print("Found " + str(len(posts)) + " results.")   
posts = pd.DataFrame(posts,columns=['title', 'score', 'subreddit', 'num_comments', 'created'])

if(args.format == "csv"):
    posts.to_csv(args.fileName + ".csv", index=False)
else:
    posts.to_json(args.fileName + ".json", default_handler=str)
    
print("Output completed.")