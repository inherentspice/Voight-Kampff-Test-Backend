import VoightKampffTestBackend.gettit as gettit
import praw
import pandas as pd

def get_top_level_posts(url):
    codes = gettit.Codes()
    reddit = praw.Reddit(
        client_id=codes.reddit_client_id,
        client_secret=codes.reddit_secret,
        password=codes.reddit_password,
        user_agent=codes.reddit_username)

    df = pd.DataFrame(columns = ['Answer'])
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=0)

    for top_level_comment in submission.comments:
        df = df.append({'Answer' : top_level_comment.body},
                ignore_index = True)
    title = submission.title
    df.to_csv(f'raw_data/{title}.csv')
    return df

def get_child_posts(url):
    codes = gettit.Codes()
    reddit = praw.Reddit(
        client_id=codes.reddit_client_id,
        client_secret=codes.reddit_secret,
        password=codes.reddit_password,
        user_agent=codes.reddit_username)

    df = pd.DataFrame(columns = ['Answer'])
    submission = reddit.submission(url=url)
    submission.comments.replace_more(limit=0)

    for comment in submission.comments.list():
        df = df.append({'Answer' : comment.body},
                ignore_index = True)
    title = submission.title
    df.to_csv(f'raw_data/{title}_all.csv')
    return df

if __name__ == '__main__':
    url = 'https://www.reddit.com/r/AskReddit/comments/vubkth/whats_a_job_thats_romanticized_but_in_reality/'
    get_top_level_posts(url=url)
    get_child_posts(url)
