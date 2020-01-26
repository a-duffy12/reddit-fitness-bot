import praw
import pdb
import re
import os
from praw.models import MoreComments as mc
import requests
from bs4 import BeautifulSoup as bs


# create reddit instance
reddit = praw.Reddit('fitness-bot')

# url access
url = 'https://www.bodybuilding.com/exercises/' # url of website to gather data
page = requests.get(url) # getting the url
soup = bs(page.content , 'html.parser') # parsing page content
urlStart = "www.bodybuilding.com" # begining of address for use in comment replies

# keywords to reply to
keys = ['neck', 'traps', 'trapezius', 'shoulders', 'shoulder', 'deltoids', 'delts', 'chest', 'pecs', 'pectorialis', 'arms', 'biceps', 'bicep', 'bis', 
'triceps', 'tris', 'tricep', 'forearms', 'forearm', 'brachioradialis', 'abs', 'ab', 'rectus abdominis', 'legs', 'quads', 'quadriceps', 'quad', 
'quadricep', 'hamstrings', 'calves', 'calf', 'gastrocnemius', 'soleus', 'lats', 'lat', 'latissimus', 'middle back', 'rhomboids', 'lower back', 
'low back', 'back']

# case if the comment reply history file does not exist
if not os.path.isfile("comment_reply_history.txt"):
    comment_reply_history = []

# case where the file does exist (default case)
else: # reading reply history to create a list of all comments replied to
    with open("comment_reply_history.txt", "r") as f: # choose file to open
        comment_reply_history = f.read() # read the file
        comment_reply_history = comment_reply_history.split("\n") # split at each new line
        comment_reply_history = list(filter(None, comment_reply_history)) # if an empty element sneaks in, it is deleted

excerciseContainer = soup.findAll("section", {"class", "exercise-list-container"}) # traverse to where the excercises are listed and linked
list = excerciseContainer[0].findAll("a") # find all the links in the sections which correspond to each address
links = [x["href"] for x in list] # stores links in an array

#used to find all the names of the links
def is_the_only_string_within_a_tag(s):
    """Return True if this string is the only child of its parent tag."""
    return (s == s.parent.string)
exercises = excerciseContainer[0].findAll(string=is_the_only_string_within_a_tag)

#create a dictionary of keys that are excercises and values that are links
excerciseDictionary = dict(zip(exercises,links))

# used for printing the dictionary
# for excercise in excerciseDictionary:
#     print(excercise + " : " + urlStart+ excerciseDictionary[excercise] )
#     print("\n")

# choosing sub to post to
subreddit = reddit.subreddit('pythonforengineers')

# check for submissions
for submission in subreddit.new(limit=1):

    # iterate through all comments in the post using a BFS
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():

        # checks to see if the bot was summoned
        if ("!exerciseFinder" in comment.body):
        
            # will run for any commenmt not previously responded to
            if comment.id not in comment_reply_history:

                comment_reply_history.append(comment.id) # adds comment to the reply history

                # check for keywords to respond to
                if any(key in comment.body for key in keys):

                    comment.reply("i have been summoned") # replies with a comment
                    print("Fitness-BOT replying to ", comment.author) # prints out what post it replied to
                
# write to comment reply history with the updated list of ids
with open("comment_reply_history.txt", "w") as f: # open file as writeable
    for comment_id in comment_reply_history: # for all the ids in the list
        f.write(comment_id + "\n") # writes the ids into the history
