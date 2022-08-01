from dataclasses import replace
import pandas as pd
import os
# import gpt_2_simple as gpt
import re


class Data:
    def __init__(self):
        pass

    def get_response(self):
        question_answers = {}
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'raw_data', 'scraped_data')
        for subdirs, dirs, files in os.walk(csv_path):
            question_answers[subdirs] = files

        data = {}

        for key, value in question_answers.items():
            if value:
                for file in value:
                    y = os.path.join(key, file)
                    data[file.replace('.csv', '')] = pd.read_csv(y)['Answer']

        return data

    def transform_training_data(self):

        data = self.get_response()

        df_topics = pd.DataFrame()
        df_trending = pd.DataFrame()
        df_questions = pd.DataFrame()

        for key, value in data.items():
            if len(key) < 12:
                df_topics[key] = value
            elif len(key) == 12:
                df_trending[key] = value
            else:
                df_questions[key] = value


        df_topics = df_topics.fillna(method='ffill')
        df_trending = df_trending.fillna(method='ffill')
        df_questions = df_questions.fillna(method='ffill')

        forbidden = ['deleted', 'cunt', 'whore', 'nigga', 'fag', 'fags', 'faggot', 'nigga', 'nigger', 'niggas', 'negro',
        'fagz', 'edit', 'slut', 'EDIT', 'Edit', 'reddit', 'skank', 'nA', 'nB', 'NB', "'>'", '>', '\\]', "'\\]'", '\\[', '<', '\\*', '-',
        'REDDIT', 'Shit,', 'Shit', 'SHIT', 'fuck', 'fucking', 'Fucking', 'fucked' , 'fuckin', 'fucken', 'fuckover', 'fucks', 'Fucks', 'FUCKS', 'Fuck',
        'Fucks', 'FUCK', "Fuckin’", 'Fuckin', 'Fucken', 'FUCk', 'fUcKiNg ', 'pretty fuccin', 'Fuccccccckkkkkk ', 'fuccckkc', 'Fucccccc. ', 'fuccboi ', 'FUCCKKK',
        'FUCCKK', 'FUCJING ', 'fuccin ']

        for words in forbidden:
            df_topics = df_topics.replace(words, '', regex=True).replace(r'http\S+', '', regex=True).replace(r'www.\S+', '', regex=True).replace(r'Www.\S+', '', regex=True).replace(r'.com\S+', '', regex=True).replace("reddit", "my guy").replace("Reddit", "My guy", regex=True).replace("Redditors", "people", regex=True).replace('shit', 'things', regex=True).replace('bullshit', 'things', regex=True).replace('fucker', 'dude', regex=True)
            df_trending = df_trending.replace(words, '', regex=True).replace(r'http\S+', '', regex=True).replace(r'www.\S+', '', regex=True).replace(r'Www.\S+', '', regex=True).replace(r'.com\S+', '', regex=True).replace("reddit", "my guy").replace("Reddit", "My guy", regex=True).replace("Redditors", "people", regex=True).replace('shit', 'things', regex=True).replace('bullshit', 'things', regex=True).replace('fucker', 'dude', regex=True)
            df_questions = df_trending.replace(words, '', regex=True).replace(r'http\S+', '', regex=True).replace(r'www.\S+', '', regex=True).replace(r'Www.\S+', '', regex=True).replace(r'.com\S+', '', regex=True).replace("reddit", "my guy").replace("Reddit", "My guy", regex=True).replace("Redditors", "people", regex=True).replace('shit', 'things', regex=True).replace('bullshit', 'things', regex=True).replace('fucker', 'dude', regex=True)

        df = df_topics.stack()
        # df = df.append(df_trending.stack())
        # df = df.append(df_questions.stack())
        df = pd.concat([df,df_trending.stack(),df_questions.stack()])

        path = "raw_data/preprocessed_data"
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Making new directory at {path}")


        df.to_csv('raw_data/preprocessed_data/training_text.csv', index=None)

        # encoded_path = 'raw_data/encoded_data'
        # if not os.path.exists(encoded_path):
        #     os.makedirs(encoded_path)
        #     print(f"Making new directory at {path}")

        # gpt.encode_csv('raw_data/preprocessed_data/training_text.csv', out_path='raw_data/encoded_data/encoded_text.csv')




if __name__ == '__main__':
    Data().transform_training_data()
