import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

stocks = ['NFTY']

ohlc = {}


def download_data():

    for stock in stocks:

        ticker = yf.Ticker(stock)
        ohlc[stock] = ticker.history(period='1y', interval='1d')['Close']

    return pd.DataFrame(ohlc)


if __name__ == '__main__':

    df = download_data()

    df['fastSMA'] = df['NFTY'].rolling(window=12).mean()
    df['slowSMA'] = df['NFTY'].rolling(window=26).mean()
    df['signal'] = df['fastSMA'] > df['slowSMA']
    df['PrevSignal'] = df['signal'].shift(1)
    df['Buy'] = (df['signal'] == 1) & (df['PrevSignal'] == 0)
    df['Sell'] = (df['signal'] == 0) & (df['PrevSignal'] == 1)
    df['invested'] = False
    is_invested = False

    for row in df.index:
        if is_invested and df['Sell'][row]:
            is_invested = False
        if not is_invested and df['Buy'][row]:
            is_invested = True

        df['invested'][row] = is_invested

    df['logReturn'] = np.log(df['NFTY']).diff()
    df['shiftedreturn'] = df['logReturn'].shift(-1)
    df['algoreturn'] = df['invested'] * df['shiftedreturn']

    df['algoreturn'].plot()
    plt.show()

    print("Algo Return = " + str(df['algoreturn'].sum()))
    print("Total Return = " + str(df['logReturn'].sum()))
