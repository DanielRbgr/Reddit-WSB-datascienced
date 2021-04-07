import datetime as dt
from psaw import PushshiftAPI

api = PushshiftAPI()

datafile = open("datasets/datadump.txt", "w", encoding="utf-8")

start_time = int(dt.datetime(2021, 3, 17).timestamp())
end_time = int(dt.datetime(2021, 3, 31).timestamp())

submissions = api.search_submissions(after=start_time,
                                     before=end_time,
                                     sort_type="created_utc",
                                     subreddit='wallstreetbets',
                                     filter=['url', 'title', 'author', 'subreddit']
                                     )

for submission in submissions:

    datafile_entry = \
        "[" + str(submission.created_utc) \
        + ";;;" + submission.title \
        + ";;;" + submission.author \
        + ";;;" + str(submission.url) + "]"

    datafile.write(datafile_entry + "\n")


print(submissions)
