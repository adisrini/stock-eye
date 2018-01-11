from pandas_datareader import data as pdr
from datetime import datetime, timedelta
from fbchat import Client
from fbchat.models import *
import fix_yahoo_finance as yf
import time
import yaml
import warnings

warnings.simplefilter("ignore", ResourceWarning)
warnings.simplefilter("ignore", DeprecationWarning)

yf.pdr_override()

tickers = ["MU", "INTC", "AMD"]
period = 100
comp_factor = 2
secrets = yaml.load(open('secrets.yaml'))
prev_closing_price = {}
prev_moving_average = {}
curr_closing_price = {}
curr_moving_average = {}

for ticker in tickers:
    prev_closing_price[ticker] = -1
    prev_moving_average[ticker] = -1

while(True):
    end = datetime.today()
    start = end - timedelta(days=comp_factor*period)

    for ticker in tickers:
        df = pdr.get_data_yahoo(ticker, start=start, end=end)

        tot = 0
        num = 0
        for i in range(0, period):
            dt = end - timedelta(days=i)
            dt_str = dt.strftime('%Y-%m-%d')
            try:
                tot += df.loc[dt_str].Close
                num += 1
            except KeyError as e:
                pass

        curr_closing_price[ticker] = df['Close'][len(df) - 1]
        curr_moving_average[ticker] = tot/num

        signal_buy = False

        if prev_moving_average[ticker] == -1:
            prev_moving_average[ticker] = curr_moving_average[ticker]

        if prev_closing_price[ticker] == -1:
            prev_closing_price[ticker] = curr_closing_price[ticker]

        if prev_closing_price[ticker] < prev_moving_average[ticker] and curr_closing_price[ticker] > curr_moving_average[ticker]:
            signal_buy = True

        print("\n")
        if(num != 0):
            print(" ==== {} ==== ".format(ticker))
            print("Moving average:            {:f}".format(tot/num))
            print("Current closing price:     {:f}".format(curr_closing_price[ticker]))
            print("Signal buy:                {:b}".format(signal_buy))

        if signal_buy:
            client = Client(secrets['email'], secrets['password'])
            client.send(Message(text="Buy {} at {}".format(ticker, curr_closing_price[ticker])), thread_id=client.uid, thread_type=ThreadType.USER)
            client.logout()

    time.sleep(600)
