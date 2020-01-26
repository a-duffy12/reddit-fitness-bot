import praw
import pdb
import re
import os
from praw.models import MoreComments

# create reddit instance
reddit = praw.Reddit('fitness-bot')

# case if the comment reply history file does not exist
if not os.path.isfile("comment_reply_history.txt"):
    comment_reply_history = []

# case where the file does exist (default case)
else: # reading reply history to create a list of all comments replied to
    with open("comment_reply_history.txt", "r") as f: # choose file to open
        comment_reply_history = f.read() # read the file
        comment_reply_history = comment_reply_history.split("\n") # split at each new line
        comment_reply_history = list(filter(None, comment_reply_history)) # if an empty element sneaks in, it is deleted

# choosing sub to post to
subreddit = reddit.subreddit('pythonforengineers')

# check for submissions
for submission in subreddit.new(limit=5):

    # iterate through all comments in the post using a BFS
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():

        if comment.id not in comment_reply_history:
            # printing the comments
            print(comment.body)

            #comment.reply("it is known") # replies with a comment
            #print("Fitness-BOT replying to ", submission.title) # prints out what post it replied to
            comment_reply_history.append(comment.id) # adds comment to the reply history

# write to comment reply history with the updated list of ids
with open("comment_reply_history.txt", "w") as f: # open file as writeable
    for comment_id in comment_reply_history: # for all the ids in the list
        f.write(comment_id + "\n") # writes the ids into the history