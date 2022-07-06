import secrets
import praw

print(secrets.reddit_client_id)
def get_top_level_posts():
    reddit = praw.Reddit(
    client_id=secrets.reddit_client_id,
    client_secret=secrets.reddit_secret,
    password=secrets.reddit_password,
    username=secrets.reddit_username)
