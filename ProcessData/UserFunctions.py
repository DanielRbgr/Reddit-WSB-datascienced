import os
import numpy as np
import pandas as pd
from GetData.StockData  import GetStockData as gsd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import GlobalDefinitions as gdef

def load_csv_data():
    # get directory of the Reddit_GME_Project folder
    dirname = os.path.dirname(os.path.dirname(__file__))
    # compose the filepath to the csv file
    filepath = os.path.join(dirname, "GetData/datasets/CSVfiles/datadump_sorted_WithNames.csv")
    # separation by semicolon is really important
    df = pd.read_csv(filepath, sep=';')
    return df

orig_df = load_csv_data()
adf = orig_df['author'].value_counts()
