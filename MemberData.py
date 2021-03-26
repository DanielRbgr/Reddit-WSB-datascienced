import pandas as pd
import os

dirname = os.path.dirname(__file__)
# compose the filepath to the csv file
filepath = os.path.join(dirname, "GetData/MemberData/Member_data.csv")

def get_wsb_suscriber():
    # load the member data, interpolate the missing ones with linear method, round to remove decimal values
    df = pd.read_csv(filepath, sep=';')
    df['date'] = pd.to_datetime(df['date'], yearfirst=True)
    df['members'] = df['members'].interpolate().round(0)
    # print(df.info)
    # print(df.dtypes)

    return df

get_wsb_suscriber()