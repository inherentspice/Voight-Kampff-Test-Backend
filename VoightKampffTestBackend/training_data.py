import pandas as pd
import os


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

        df = df.fillna(method='ffill')

        data.to_csv('raw_data/training_files.txt', header=None, index=None, sep=' ', mode='a')

        return




if __name__ == '__main__':
    print(Data().get_response())
