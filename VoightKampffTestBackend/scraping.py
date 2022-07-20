import VoightKampffTestBackend.gettit as gettit
import praw
import pandas as pd
import time
import os

class Reddit:
    def __init__(self):
        #instantiate the scraper and get authentification
        self.codes = gettit.Codes()
        self.reddit = praw.Reddit(client_id = self.codes.reddit_client_id,
                                           client_secret = self.codes.reddit_secret,
                                           password = self.codes.reddit_password,
                                           user_agent = self.codes.reddit_username)

    def get_child_posts(self, url, topic='qanda'):
        """Writes the top-rated comments from a r/AskReddit thread
        to a csv file. It will create a directory named the variable
        saved under topic, and the file will be the title of the
        reddit thread. Function required the url for the reddit
        thread you want to scrape."""

        #create directory if it does not exist
        path = f'raw_data/scraped_data/{topic}'
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Making new directory at {path}")

        #create pandas DataFrame to store data
        df = pd.DataFrame(columns = ['Answer'])


        link = self.reddit.submission(url=url)

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


    def get_hot_posts(self, subreddit='AskReddit'):
        """Collects the top ten trending posts on a subreddit, and
        writes the top-rated comments to a csv file. It will create
        a directory named 'misc', and the file will be the title of the
        first twelve characters of the reddit thread. Function will default
        scrape r/AskReddit unless a different subreddit is passed as a string."""


        #create directory 'misc' if it does not exist
        path = f'raw_data/scraped_data/misc'
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Making new directory at {path}")

        #create variable 'posts' to store urls
        posts = []

        link = self.reddit.subreddit(subreddit)

        #loop through popular posts in 'subreddit' and
        #store the url in 'posts'
        for post in link.hot(limit=10):
            posts.append(post.url)

        #loop through urls and pass each to get_child_posts
        #function to scrape comments
        for post in posts:
            print(f"Getting answers from post")
            self.get_child_posts(post, topic="misc")
            time.sleep(0.10)


    def search_by_keyword(self, subreddit="all", search_term="wealth", limit=1000):
        """Searches 'all' subreddits for a search_term in the title, and
        scrapes the top comments from 'limit' posts. Results are written
        into one csv file with the name of the search term."""


        #create directory 'topics' if it does not exist
        path = f"raw_data/scraped_data/topics"
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Making new directory at {path}")

        file_path = f"raw_data/scraped_data/topics/{search_term}.csv"

        #checks if search_term has already been scraped and
        #ends function if so
        if os.path.isfile(file_path):
            print(f"{search_term}.csv already exists...")
            return

        link = self.reddit.subreddit(subreddit)

        #create DataFrame to store comments
        df = pd.DataFrame(columns=['Answer'])

        #loop through comments in each url and append
        #results to 'df'
        for post in link.search(search_term, limit=limit):
            post.comments.replace_more(limit=0)
            print(f"Getting comments from {post.title}")
            for comment in post.comments.list():
                df = df.append({'Answer' : comment.body},
                    ignore_index = True)
            time.sleep(0.10)

        #write results to csv named after the search_term
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
        Reddit().get_child_posts(url=i)

    Reddit().get_hot_posts()

    TOPICS = ["wealth", "rich", "lottery", "Bezos", "quality of life", "improve life", "health", "worst alcohol", "tequila"]
    for i in TOPICS:
        Reddit().search_by_keyword(search_term=i)
