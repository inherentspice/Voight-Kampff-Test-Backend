import pandas as pd

df = pd.read_csv ('raw_data/Whats_a_job_thats_romanticized_but_in_reality_sucks?_all.csv')


class Response:
    def __init__(self):
        self.data = df['Answer'].get_data()

    def get_response(self):
        responses = self.data['Answer'].copy()
        return responses

print (Response.get_response(df))
