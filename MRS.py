import requests
import json
import csv
import argparse, sys
import time
import datetime
import tkinter

def getPushshiftData(query, sub, after, before):
    url = 'https://api.pushshift.io/reddit/search/submission/?title=' + str(query) + '&size=1000'  + '&subreddit=' + str(sub)
    
    if after != 0:
        url += '&after=' + str(after)
        
    if before != 0:
        url += '&before=' + str(before)
        
    r = requests.get(url)
    if not '<html>' in r.text:
        data = json.loads(r.text)
        return data['data']
    else:
        return None

def collectSubData(subm, subStats):
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

def updateSubs_file(filename, subStats):
    upload_count = 0
    file = filename + ".csv"
    print("Saving to " + str(file))
    with open(file, 'w', newline='', encoding='utf-8') as file: 
        a = csv.writer(file, delimiter=',')
        headers = ["Post ID","Title","Url","Author","Score","Publish Date","Total No. of Comments","Permalink","Flair"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count+=1
            
        print(str(upload_count) + " submissions have been saved to file.")

def dateToInt(date):
    return int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()))

def startSearch(query, after, before, sub, filename, statusText, tk):
    statusText.delete('1.0', tkinter.END)
    statusText.insert(tkinter.END, "Fetching data.\n")
    tk.update()

    data = getPushshiftData(query, after, before, sub)
    totalLength = 0
    subCount = 0
    subStats = {}

    statusText.insert(tkinter.END, "Converting data.\n")
    tk.update()

    if data:
        while len(data) > 0:
            for submission in data:
                collectSubData(submission, subStats)
                subCount+=1
                
            statusText.insert(tkinter.END, "Added results until " + str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])) + "\n")
            tk.update()

            after = data[-1]['created_utc']
            totalLength += len(data)
            data = getPushshiftData(query, after, before, sub)
        
        statusText.insert(tkinter.END, "Found %s results.\n" % totalLength)
        statusText.insert(tkinter.END, "Completed.", "success")
        tk.update()

        updateSubs_file(filename, subStats)
    else:
        statusText.insert(tkinter.END, "No data found.", "fail")