import pandas as pd
import os
import gpt_2_simple as gpt


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

        for key, value in data.items():
            if len(key) == 12:
                print(value)
            elif len(key) < 12:
                pass
            else:
                pass

        #slurs = ["fuck", "shit", " shitty", "anal", "asshole", "dick", "dickhead", "wanker", "prick", "fuckhead","fucking"
                 #"deepshit", "cum", "cumhead", "twat", "cunt", "pussy", "vagina", "whore", "slut", "slutty", "sonofabitch", 'testicles',
                 #"skank", "skanky", "skanks", "screw", "sex", "sexx", "sexxx", "xxx", "queer", "puta", "poo", "poop", "poes", "porn",
                 #"nigga", "nigger", "niggas", "negro", "negros", "nikka", "nikkas", "paki", "orgasm", "redneck", "motherfucker", "mofo", "masturbate",
                 #"masturbates", "masturbating", "lesbian", "lesbo", "trans", "transgender", "knob", "knobs", "knobz", "jizz", "jerkoff", "fag", "faggot",
                 #"fags", "fagz", "faggots"]


        # df = data.fillna(method='ffill')

        #.astype(str)

        #censored = profanity.censor(df, 'heck')

        #str_to_df = censored.DataFrame()


        # df.to_csv('raw_data/training_files.txt', header=None, index=None, sep=' ', mode='a')

        # with open('raw_data/training_files.txt', 'r') as f, open('raw_data/training_files_edited.txt', 'w') as fo:
        #     for line in f:
        #         fo.write(line.replace('reddit', 'my guy').replace("edit:", "").replace("Edit:", "").replace("fucking", "so").replace('"', " ")
        #                  .replace('FUCK', "HELL").replace('fuckin', "nice").replace('fuck', "hell").replace('Fuck', "Hell").replace('[deleted]', "")
        #                  .replace('[removed]', "").replace('shit', "things").replace('shitty', "not nice").replace('ass', "behind")
        #                  .replace('asshole', "person").replace('an asshole', "a person"))

            #for v in slurs:
                #str.replace("", "nice")

        return




if __name__ == '__main__':
    # print(Data().get_response())
    Data().transform_training_data()
