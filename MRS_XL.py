import pandas as pd
import requests
import json
import csv
import argparse, sys
import time
import datetime

def getPushshiftData(query, after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/submission/?title='+str(query)+'&size=1000&after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)
    r = requests.get(url)
    if not '<html>' in r.text:
        data = json.loads(r.text)
        return data['data']
    else:
        print('error.')
        return None

def collectSubData(subm):
    subData = list() #list to store data points
    title = subm['title']
    url = subm['url']
    try:
        flair = subm['link_flair_text']
    except KeyError:
        flair = "NaN"    
    author = subm['author']
    sub_id = subm['id']
    score = subm['score']
    created = datetime.datetime.fromtimestamp(subm['created_utc']) #1520561700.0
    numComms = subm['num_comments']
    permalink = subm['permalink']
    
    subData.append((sub_id,title,url,author,score,created,numComms,permalink,flair))
    subStats[sub_id] = subData

def updateSubs_file():
    upload_count = 0
    print("input filename of submission file")
    filename = input()
    file = filename + ".csv"
    with open(file, 'w', newline='', encoding='utf-8') as file: 
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID","Title","Url","Author","Score","Publish Date","Total No. of Comments","Permalink","Flair"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1
            
        print(str(upload_count) + " submissions have been uploaded")

def dateToInt(date):
    return int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))

parser=argparse.ArgumentParser()

parser.add_argument('--subr', help='name of subreddit to search in', default='all')
parser.add_argument('--keyword', help='keyword to search for', default='_')
parser.add_argument('--after', help='first date to find results for, format YYYY-MM-DD, example: 2020-01-01', default=0)
parser.add_argument('--before', help='last date to find results for', default=0)

args=parser.parse_args()
    
#Subreddit to query
sub = args.subr
#before and after dates
after = "1514764800"  #January 1st 
before = "1538352000" #October 1st

if not args.after == 0:
    after = dateToInt(args.after)
else:
    after = args.after
    
if not args.before == 0:
    before = dateToInt(args.before)
else:
    before = args.before
    
query = args.keyword
subCount = 0
subStats = {}

data = getPushshiftData(query, after, before, sub)
totalLength = 0

if data:
    while len(data) > 0:
        for submission in data:
            collectSubData(submission)
            subCount+=1
        print("Added results until " + str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
        after = data[-1]['created_utc']
        totalLength += len(data)
        data = getPushshiftData(query, after, before, sub)
    
    print(totalLength)
    updateSubs_file()