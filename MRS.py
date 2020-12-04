import pandas as pd
import praw
import json
import time
import datetime
import sys
from praw.models.listing.mixins import subreddit

analyzedPosts = 100
mode = 0
    
if len(sys.argv) > 3:
    (_, subreddit, mode, keyword, analyzedPosts) = sys.argv
else:
    (_, subreddit, mode, keyword) = sys.argv
    
mode = int(mode)

reddit = praw.Reddit(client_id='97BU0LvRgn4Auw', 
                    client_secret='7E7dIRJbzqIZZyKhnstA4UrrU8YZgg', 
                    user_agent='CLAS Scrapper')
    
posts = []

print("Starting to look for " + keyword + " in " + subreddit)

if mode == 0:
    for post in reddit.subreddit(subreddit).top(limit=int(analyzedPosts)):
        if(post.link_flair_text == keyword):
            posts.append([post.title, post.score, post.subreddit, post.num_comments, 
                          datetime.datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S')])

if mode == 1:
    for post in reddit.subreddit(subreddit).top(limit=int(analyzedPosts)):
        if(keyword in post.title):
            posts.append([post.title, post.score, post.subreddit, post.num_comments, 
                          datetime.datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S ')])
            
if mode == 2:
    for post in reddit.subreddit(subreddit).top(limit=int(analyzedPosts)):
        if(keyword in post.title):
            posts.append([post.title, post.score, post.subreddit, post.num_comments, 
                          datetime.datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S ')])

print("Found " + str(len(posts)) + " results.")   
posts = pd.DataFrame(posts,columns=['title', 'score', 'subreddit', 'num_comments', 'created'])
    
posts.to_csv("scrap.csv", index=False)