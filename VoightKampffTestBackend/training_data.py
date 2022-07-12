import pandas as pd
import os


class Data:
    def __init__(self):
        pass

    def get_response(self):
        csv_path = 'raw_data/scraped_data'
        file_names = [f for f in os.listdir(csv_path) if f.endswith('.csv')]
        files = file_names.copy()

        for i, j in enumerate(file_names):
            file_names[i] = j.replace('_all.csv', '')

        data = pd.DataFrame()

        for (x, y) in zip(file_names, files):
            y = os.path.join(csv_path, y)
            data[x] = pd.read_csv(y)['Answer']

        return data


if __name__ == '__main__':
    print(Data().get_response())
