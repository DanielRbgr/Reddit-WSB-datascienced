import praw

#Definition der Reddit Parameter
#für read-only wären Useraccount und Passwort eigentlich nicht nötig
reddit_client_id = "PJ_uX7M9GHU8yw"
reddit_client_secret = "EEDT2Kg0-w4iQQrgQIGE9k3SFCMnag"
reddit_useraccount = "thec00p"
reddit_userpasswort = "D4nn7123"
reddit_useragent = "data-script by u/thec00p"

datafile = open("datasets/DumpArchive/datadump.txt", "w", encoding="utf-8")

#erzeugen der Reddit-Instanz einschl. subredit
reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     password=reddit_userpasswort,
                     user_agent=reddit_useragent,
                     username=reddit_useraccount)
subreddit = reddit.subreddit("wallstreetbets")

#Checking if everything was succesfull
print(reddit.user.me())
print(subreddit.display_name)  # output: redditdev


for submission in subreddit.new(limit = 1000000):

    datafile_entry = \
        "[" + str(submission.created_utc) \
        +";;;" +submission.title \
        +";;;" +str(submission.url) +"]"

    #print(submission.created_utc)
    #print(submission.title)  # Output: the submission's title
    #print(submission.id)     # Output: the submission's ID
    #print(submission.score)  # Output: the submission's score
    #print(submission.num_comments)    #

    #print(datafile_entry)
    datafile.write(datafile_entry +"\n")

#closing the datafile at the end
datafile.close()