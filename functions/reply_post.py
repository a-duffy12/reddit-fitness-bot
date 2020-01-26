import praw
import pdb
import re
import os

# create reddit instance
reddit = praw.Reddit('fitness-bot')

# case if the post reply history file does not exist
if not os.path.isfile("post_reply_history.txt"):
    post_reply_history = []

# case where the file does exist (default case)
else: # reading reply history to create a list of all posts replied to
    with open("post_reply_history.txt", "r") as f: # choose file to open
        post_reply_history = f.read() # read the file
        post_reply_history = post_reply_history.split("\n") # split at each new line
        post_reply_history = list(filter(None, post_reply_history)) # if an empty element sneaks in, it is deleted

# choosing sub to post to
subreddit = reddit.subreddit('pythonforengineers')

# check for submissions
for submission in subreddit.hot(limit=5):
    print("Title: ", submission.title)
    print("Score: ", submission.score)
    print("---------------------------------\n")

    # check to see if the post id already exists in the reply history
    if submission.id not in post_reply_history:

        # if it has not been replied to yet, check posts (case insensitive)
        if re.search("i love python", submission.title, re.IGNORECASE):

            submission.reply("it is known") # replies with a comment
            print("Fitness-BOT replying to ", submission.title) # prints out what post it replied to
            post_reply_history.append(submission.id) # adds post to the reply history

# write to reply history with the updated list of ids
with open("post_reply_history.txt", "w") as f: # open file as writeable
    for post_id in post_reply_history: # for all the ids in the list
        f.write(post_id + "\n") # writes the ids into the history
