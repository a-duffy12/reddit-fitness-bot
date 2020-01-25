#!/usr/bin/python
import praw

reddit = praw.Reddit('bot1')

#use r/pythonforengineers if just fucking around (or posting)
subreddit = reddit.subreddit("fitness")

for submission in subreddit.hot(limit=5): #.tab chooses which tab to browse
    print("Title: ", submission.title)
    print("Text: ", submission.selftext)
    print("Score: ", submission.score)
    print("---------------------------------\n")
