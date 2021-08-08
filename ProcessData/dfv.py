import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import GlobalDefinitions as gdef


def load_csv_data(file):
    # get directory of the Reddit_GME_Project folder
    dirname = os.path.dirname(os.path.dirname(__file__))
    # compose the filepath to the csv file
    secondpath = "GetData/dfv/" + file
    filepath = os.path.join(dirname, secondpath)
    df = pd.read_csv(filepath, sep=';', header=None)
    return df


"------------------------------Cash + Total Worth--------------------------------------------------------------"
def print_cash_total_worth():
    dfv_worth = load_csv_data('dfv_worth.csv')
    dfv_worth = dfv_worth.T
    dfv_worth.columns=(['date', 'stock', 'Jan15at10', 'Jan15at15', 'Jan15at17', 'Jan15at20', 'Apr16at12', 'cash', 'total'])

    x = pd.Series(dfv_worth['date'].T)

    c = 0
    for i in x:
        x[c] = datetime.strptime(i, '%d.%m.%Y')
        c += 1

    plt.plot(x, dfv_worth['cash'].astype('float64')/1e6, color='#85bb65', marker='o', label='cash')
    plt.plot(x, dfv_worth['total'].astype('float64')/1e6, color='darkslateblue', marker='o', label='total')
    plt.title("DeepFuckingValue: Cash and total portfolio development", fontdict=gdef.font_title, pad=20)
    plt.ylabel("Value [mio. $]", fontdict=gdef.font_label, fontsize='xx-large', labelpad=10)
    plt.xlabel("Date", fontdict=gdef.font_label, fontsize='xx-large', labelpad=10)
    plt.legend(fontsize='xx-large')
    plt.xticks(fontsize='xx-large')
    plt.yticks(fontsize='xx-large')
    plt.grid()
    plt.show()


"--------------------------------------------Single Position----------------------------------------------------"
# possible positions: stock, Jan 15 21@10, Jan 15 21@15, Jan 15 21@17, Jan 15 21@20, Apr 16 21@12
def print_single_position(position):

    position_value = position +"v"
    position_quantity = position +"q"

    dfv_positions = load_csv_data('dfv_positions.csv')
    dfv_positions = dfv_positions.T
    dfv_positions.columns = dfv_positions.iloc[0, :]
    dfv_positions = dfv_positions.iloc[1:-1, :]

    x = pd.Series(dfv_positions['date'].T)
    c = 0
    for i in x:
        c += 1
        x[c] = datetime.strptime(i, '%d.%m.%Y')

    fig, ax1 = plt.subplots(figsize=(12, 12))
    plt.xticks(fontsize='xx-large')
    plt.xlabel("Date", fontdict=gdef.font_label, labelpad=10)
    plt.xlim(x.iloc[0], x.iloc[-1])
    # -------------price per positition----------------------------------------
    ax1.plot(x, dfv_positions[position_value].astype('float64'),
                  color='firebrick', linewidth=3, marker='o')
    plt.ylim(0, 500)
    plt.ylabel("Share price[$]", fontdict=gdef.font_label, labelpad=10)
    ax1.legend(['price per share'], loc=2, fontsize='xx-large')
    plt.yticks(fontsize='xx-large')
    plt.grid()
    # -------------position size------------------------------------------------
    ax2 = ax1.twinx()
    ax2.bar(x, dfv_positions[position_quantity].astype('float64'), color='slategrey')
    plt.ylabel("Quantity", fontdict=gdef.font_label, labelpad=10)
    plt.ylim(0, 2000)
    chart_title = "DeepFuckingValue Performance: " +position +"$"
    plt.title(chart_title, fontdict=gdef.font_title, pad=20)
    ax2.legend(['quantity'], loc=1, fontsize='xx-large')
    plt.yticks(fontsize='xx-large')
    # that ax1 is displayed in front of ax2
    ax1.set_zorder(ax2.get_zorder()+1)
    ax1.patch.set_visible(False)
    plt.show()


"--------------------------------------------All positions----------------------------------------------------"
def print_all_positions():
    dfv_positions = load_csv_data('dfv_positions.csv')
    dfv_positions = dfv_positions.T
    dfv_positions.columns = dfv_positions.iloc[0, :]
    dfv_positions = dfv_positions.iloc[1:-1, :]

    x = pd.Series(dfv_positions['date'].T)
    c = 0
    for i in x:
        c += 1
        x[c] = datetime.strptime(i, '%d.%m.%Y')

    fig, ax1 = plt.subplots(figsize=(12, 12))
    plt.xticks(fontsize='xx-large')
    plt.xlabel("Date", fontdict=gdef.font_label, labelpad=10)
    width=0.3
    # -------------price per positition----------------------------------------
    plt.plot(x, dfv_positions["Jan 15 21@10q"].astype('float64'), zorder=5, linewidth=1, color='firebrick')
    plt.plot(x, dfv_positions["Jan 15 21@15q"].astype('float64'), zorder=4, linewidth=2,color='b')
    plt.plot(x, dfv_positions["Jan 15 21@17q"].astype('float64'), zorder=3, linewidth=3, color='g')
    plt.plot(x, dfv_positions["Jan 15 21@20q"].astype('float64'), zorder=2, linewidth=4, color='c')
    plt.plot(x, dfv_positions["Apr 16 21@12q"].astype('float64'), zorder=1, linewidth=5, color='k')
    plt.ylabel("Share price[$]", fontdict=gdef.font_label, labelpad=10)
    plt.yticks(fontsize='xx-large')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    # possible positions: stock, Jan 15 21@10, Jan 15 21@15, Jan 15 21@17, Jan 15 21@20, Apr 16 21@12
    print_single_position("Jan 15 21@10")