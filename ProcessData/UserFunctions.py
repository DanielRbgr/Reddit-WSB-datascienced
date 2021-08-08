import os
import pandas as pd


def load_csv_data():
    # get directory of the Reddit_GME_Project folder
    dirname = os.path.dirname(os.path.dirname(__file__))
    # compose the filepath to the csv file
    filepath = os.path.join(dirname, "GetData/datasets/CSVfiles/datadump_sorted_WithNames.csv")
    # separation by semicolon is really important
    df = pd.read_csv(filepath, sep=';')
    return df


if __name__ == '__main__':
    # orig_df = load_csv_data()
    print("UserData loaded")

