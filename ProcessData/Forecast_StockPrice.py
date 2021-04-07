import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from datetime import datetime as dt
import ProcessData.TitleFunctions as tf
import GlobalDefinitions as gdef
from GetData.StockData import GetStockData as gsd

from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM

starttime = gdef.firsttimstamp
endtime = 1617141592
testborder = datetime.date(2021, 2, 28)
# ---------------------------------------------- Generate Data ---------------------------------------------------------
# load the DataFrame with the
df_mentions = tf.display_buzzword("GME", starttime, endtime)
df_mentions.day = df_mentions.day.astype('int32')
df_mentions.day = pd.to_datetime(df_mentions.day, unit='s') + pd.Timedelta('01:00:00')
df_mentions['mentions'].replace(np.nan, 0.0, inplace=True)
df_mentions.mentions = df_mentions.mentions.astype(np.float32)

df_stockprice = gsd.GetStockData("GME", dt.utcfromtimestamp(starttime).strftime('%Y-%m-%d'),
                                 dt.utcfromtimestamp(endtime).strftime('%Y-%m-%d'))
df_stockprice.reset_index(level=0, inplace=True)
df_stockprice = df_stockprice.drop(['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], axis=1)
df_stockprice = df_stockprice.rename(columns={"Date":"day"})

df_merged = pd.merge(df_stockprice, df_mentions, on=['day'], how='inner')
df_merged['restriction'] = (df_merged.day >= pd.to_datetime(datetime.date(2021, 1, 28))) & \
                            (df_merged.day < pd.to_datetime(datetime.date(2021, 2, 5)))
df_merged['restriction'] = df_merged['restriction'].astype(np.float32)

#scaler = MinMaxScaler(feature_range=(0,1))
#df_merged['mentions'] = scaler.fit_transform(df_merged['mentions'].values.reshape(-1, 1))
#df_merged['Close'] = scaler.fit_transform(df_merged['Close'].values.reshape(-1, 1))

scaler = StandardScaler()
df_merged['mentions'] = scaler.fit_transform(df_merged['mentions'].values.reshape(-1, 1))
df_merged['Close_scal'] = scaler.fit_transform(df_merged['Close'].values.reshape(-1, 1))

train, test = df_merged.loc[df_merged['day'] <= pd.to_datetime(testborder)],\
              df_merged.loc[df_merged['day'] > pd.to_datetime(testborder)]

prediction_days = 3

# prepare the train data
x_train = []
y_train = []

for x in range(prediction_days, len(train.Close_scal)):
    x_train.append(train.Close_scal[x-prediction_days:x].values)
    y_train.append(train.Close_scal[x])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# prepare the test data
x_test = []
y_test = []

test = test.reset_index(drop=True)

for x in range(prediction_days, len(test.Close_scal)):
    x_test.append(test.Close_scal[x-prediction_days:x].values)
    y_test.append(test.Close_scal[x])

x_test, y_test = np.array(x_test), np.array(y_train)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

#Build the Model

model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))  #Prediction of next closing value

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=25, batch_size=32)

predicted_price = model.predict(x_test)
predicted_price = scaler.inverse_transform(predicted_price)

df_stockprice = df_stockprice.loc[df_stockprice['day'] >= pd.to_datetime(testborder)]
df_stockprice = df_stockprice.reset_index(drop=True)

# Plot the test prediciton
plt.plot(df_stockprice.Close, color='k')
plt.plot(predicted_price, color='green')
plt.show()

print(df_stockprice.shape)

