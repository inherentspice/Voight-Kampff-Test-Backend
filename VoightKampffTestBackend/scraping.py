import VoightKampffTestBackend.gettit as gettit
import praw
import pandas as pd
import time
import os

def get_child_posts(url, topic='qanda'):
    """Writes the top-rated comments from a r/AskReddit thread
    to a csv file. It will create a directory named the variable
    saved under topic, and the file will be the title of the
    reddit thread. Function required the url for the reddit
    thread you want to scrape."""

    # instantiate the scraper and authenticate.
    codes = gettit.Codes()
    reddit = praw.Reddit(
        client_id=codes.reddit_client_id,
        client_secret=codes.reddit_secret,
        password=codes.reddit_password,
        user_agent=codes.reddit_username)

    #create directory if it does not exist
    path = f'raw_data/scraped_data/{topic}'
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Making new directory at {path}")

    #create pandas DataFrame to store data
    df = pd.DataFrame(columns = ['Answer'])


    link = reddit.submission(url=url)
    link.comments.replace_more(limit=0)

    #loop through top-level comments in the reddit thread
    #and append to DataFrame
    for comment in link.comments.list():
        df = df.append({'Answer' : comment.body},
                ignore_index = True)

    #short title if it is not
    if topic=="qanda":
        title = link.title
    else:
        title = link.title[0:12]

    #If '/' in title of thread, it will be read as a new directory
    title = title.replace("/", "")

    #write DataFrame to a csv
    df.to_csv(f'raw_data/scraped_data/{topic}/{title}.csv')
    return df

def get_hot_posts(subreddit='AskReddit'):
    """Collects the top ten trending posts on a subreddit, and
    writes the top-rated comments to a csv file. It will create
    a directory named 'misc', and the file will be the title of the
    first twelve characters of the reddit thread. Function will default
    scrape r/AskReddit unless a different subreddit is passed as a string."""

    # instantiate the scraper and authenticate.
    codes = gettit.Codes()
    reddit = praw.Reddit(
        client_id=codes.reddit_client_id,
        client_secret=codes.reddit_secret,
        password=codes.reddit_password,
        user_agent=codes.reddit_username)

    #create directory 'misc' if it does not exist
    path = f'raw_data/scraped_data/misc'
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Making new directory at {path}")

    #create variable 'posts' to store urls
    posts = []

    link = reddit.subreddit(subreddit)

    #loop through popular posts in 'subreddit' and
    #store the url in 'posts'
    for post in link.hot(limit=10):
        posts.append(post.url)

    #loop through urls and pass each to get_child_posts
    #function to scrape comments
    for post in posts:
        print(f"Getting answers from post")
        get_child_posts(post, topic="misc")
        time.sleep(0.10)

def search_by_keyword(subreddit="all", search_term="wealth", limit=1000):
    codes = gettit.Codes()
    reddit = praw.Reddit(
        client_id=codes.reddit_client_id,
        client_secret=codes.reddit_secret,
        password=codes.reddit_password,
        user_agent=codes.reddit_username)

    path = f"raw_data/scraped_data/topics"
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Making new directory at {path}")

    file_path = f"raw_data/scraped_data/topics/{search_term}.csv"

    if os.path.isfile(file_path):
        print(f"{search_term}.csv already exists...")
        return

    link = reddit.subreddit(subreddit)

    df = pd.DataFrame(columns=['Answer'])

    for post in link.search(search_term, limit=limit):
        post.comments.replace_more(limit=0)
        print(f"Getting comments from {post.title}")
        for comment in post.comments.list():
            df = df.append({'Answer' : comment.body},
                    ignore_index = True)
        time.sleep(0.10)
    df.to_csv(f'raw_data/scraped_data/topics/{search_term}.csv')



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
        get_child_posts(url=i)

    get_hot_posts()

    TOPICS = ["wealth", "rich", "lottery", "Bezos"]
    for i in TOPICS:
        search_by_keyword(search_term=i)
