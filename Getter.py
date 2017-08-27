import praw
from credentials import AWS_ACCESS_KEY, AWS_BUCKET_NAME, AWS_SECRET_KEY, CLIENT_ID, CLIENT_SECRET, USER_AGENT
import time
import io
import json
python Getter.py
#gain authorization to scan reddit through praw
reddit = praw.Reddit(client_id= CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent= USER_AGENT)
counter = 0
texts = []
urls = []
for submission in reddit.subreddit('nottheonion').top('day'):
    if counter == 3:
        break
    else:
        texts.append(submission.title)
        urls.append(submission.url)
        counter += 1

titlelist = []
counter = 0
for title in texts:
    date = time.strftime("%Y-%m-%dT%H:%M:%S.0Z")
    titlelist.append({'uid':counter,'updateDate':date,'titleText':title,'mainText':title, 'redirectionURL': urls[counter]})
    counter += 1

#checks for version control
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

with io.open('data.json', 'w', encoding='utf8') as outfile:
    print("Writing to JSON file...")
    str_ = json.dumps(titlelist,
                      indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))

    print("Write successful. \n")