import code

from requests_toolbelt import user_agent
import praw
import pandas as pd

def get_top_level_posts(url):
    reddit = praw.Reddit(
        client_id=code.reddit_client_id,
        client_secret=code.reddit_secret,
        password=code.reddit_password,
        user_agent=code.reddit_username)

    df = pd.DataFrame(columns = ['Answer'])
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=0)

    for top_level_comment in submission.comments:
        df = df.append({'Answer' : top_level_comment.body},
                ignore_index = True)

    return df

if __name__ == '__main__.py':
    url = 'https://www.reddit.com/r/AskReddit/comments/vnkxce/whats_a_weird_smell_youre_willing_to_admit_you/'
    print(get_top_level_posts(url=url))