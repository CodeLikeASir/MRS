import pandas as pd
import praw
import json
import time
import datetime
import configparser
import sys
from praw.models.listing.mixins import subreddit

def checkDate(first, last, date):
    return date > first and date < last

configParser = configparser.RawConfigParser()   
configFilePath = r'config.txt'
configParser.read(configFilePath)

reddit = praw.Reddit(client_id=configParser.get('api-key', 'client_id'), 
                    client_secret=configParser.get('api-key', 'client_secret'), 
                    user_agent=configParser.get('api-key', 'user_agent'))
 
analyzedPosts = 100
mode = 0
start = 0
end = 0

if len(sys.argv) > 5:
    (_, subreddit, mode, keyword, start, end, analyzedPosts) = sys.argv
    start = time.mktime(datetime.datetime.strptime(start, "%Y-%m-%d").timetuple())
    end = time.mktime(datetime.datetime.strptime(end, "%Y-%m-%d").timetuple())
elif len(sys.argv) > 3:
    (_, subreddit, mode, keyword, analyzedPosts) = sys.argv
else:
    (_, subreddit, mode, keyword) = sys.argv
    
mode = int(mode)
    
posts = []

print("Starting to look for " + keyword + " in " + subreddit)

if mode == 0:
    for post in reddit.subreddit(subreddit).top(limit=int(analyzedPosts)):
        if(post.link_flair_text == keyword):
            if(start > 0 and checkDate(start, end, post.created_utc)):
                posts.append([post.title, post.score, post.subreddit, post.num_comments, 
                          datetime.datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d')])

if mode == 1:
    for post in reddit.subreddit(subreddit).top(limit=int(analyzedPosts)):
        if(keyword in post.title):
            if(start > 0 and checkDate(start, end, post.created_utc)):
                posts.append([post.title, post.score, post.subreddit, post.num_comments, 
                          datetime.datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d')])

print("Found " + str(len(posts)) + " results.")   
posts = pd.DataFrame(posts,columns=['title', 'score', 'subreddit', 'num_comments', 'created'])
    
posts.to_csv("scrap.csv", index=False)