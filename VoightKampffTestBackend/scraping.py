import VoightKampffTestBackend.gettit as gettit
import praw
import pandas as pd
import time

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
    title = title.replace("/", "")
    df.to_csv(f'raw_data/scraped_data/{title}.csv')
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
    df.to_csv(f'raw_data/scraped_data/{title}_all.csv')
    return df

def get_hot_posts(subreddit='AskReddit'):
    codes = gettit.Codes()
    reddit = praw.Reddit(
        client_id=codes.reddit_client_id,
        client_secret=codes.reddit_secret,
        password=codes.reddit_password,
        user_agent=codes.reddit_username)

    posts = []
    ml_subreddit = reddit.subreddit(subreddit)
    for post in ml_subreddit.hot(limit=10):
        posts.append(post.url)
    for i in posts:
        print(f"Getting answers...")
        get_top_level_posts(i)
        time.sleep(0.10)

if __name__ == '__main__':
    URLS = ["https://www.reddit.com/r/AskReddit/comments/vo73uc/whats_a_weird_thing_you_think_only_you_do/",
            "https://www.reddit.com/r/AskReddit/comments/vjpkye/the_supreme_court_has_overturned_roe_v_wade_how/?utm_source=share&utm_medium=web2x&context=3 ",
            "https://www.reddit.com/r/AskReddit/comments/pbzt5b/what_improved_your_quality_of_life_so_much_you/?utm_source=share&utm_medium=web2x&context=3 ",
            "https://www.reddit.com/r/AskReddit/comments/vwdq67/you_can_get_the_attention_of_the_whole_planet_but/",
            "https://www.reddit.com/r/AskReddit/comments/vwd8zd/if_you_could_have_the_answer_to_one_question_what/",
            "https://www.reddit.com/r/AskReddit/comments/vw7f2d/whats_the_worst_alcoholic_beverage/",
            "https://www.reddit.com/r/AskReddit/comments/vvauxe/every_country_is_an_animal_what_animal_is_your/",
            "https://www.reddit.com/r/AskReddit/comments/osoje1/you_wake_up_tomorrow_with_jeff_bezos_current_net/",
            "https://www.reddit.com/r/AskReddit/comments/oqofqj/without_saying_the_name_whats_your_favorite_video/",
            ]

    for i in URLS:
        # get_child_posts(url=i)
        get_hot_posts()
