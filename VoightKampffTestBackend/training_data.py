from operator import index
import pandas as pd
import os
from better_profanity import profanity


class Data:
    def __init__(self):
        pass

    def get_response(self):
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'raw_data', 'scraped_data')
        file_names = [f for f in os.listdir(csv_path) if f.endswith('.csv')]
        files = file_names.copy()

        for i, j in enumerate(file_names):
            file_names[i] = j.replace('_all.csv', '')

        data = pd.DataFrame()

        for (x, y) in zip(file_names, files):
            y = os.path.join(csv_path, y)
            data[x] = pd.read_csv(y)['Answer']

        return data

    def transform_training_data(self):

        data = self.get_response()
        #slurs = {"fuck", "shit", " shitty", "anal", "asshole", "dick", "dickhead", "wanker", "prick", "fuckhead",
                # "deepshit", "cum", "cumhead", "twat", "cunt", "pussy", "vagina", "whore", "slut", "slutty", "sonofabitch", 'testicles',
                 #"skank", "skanky", "skanks", "screw", "sex", "sexx", "sexxx", "xxx", "queer", "puta", "poo", "poop", "poes", "porn",
                 #"nigga", "nigger", "niggas", "negro", "negros", "nikka", "nikkas", "paki", "orgasm", "redneck", "motherfucker", "mofo", "masturbate",
                 #"masturbates", "masturbating", "lesbian", "lesbo", "trans", "transgender", "knob", "knobs", "knobz", "jizz", "jerkoff", "fag", "faggot",
                 #"fags", "fagz", "faggots"}

        data = data.replace(("reddit", "my guy"),
                             ("Edit", " "))

        df = data.fillna(method='ffill')

        #.astype(str)

        #censored = profanity.censor(df, 'heck')

        #str_to_df = censored.DataFrame()


        #censored.to_csv('raw_data/training_files.txt', header=None, index=None, sep=' ', mode='a')

        return




if __name__ == '__main__':
    print(Data().get_response())
    Data().transform_training_data()
