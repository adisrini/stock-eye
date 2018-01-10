from pandas_datareader import data as pdr
from datetime import datetime, timedelta
import fix_yahoo_finance as yf
import time

yf.pdr_override()

ticker = "MU"
period = 100
comp_factor = 2

while(True):
    end = datetime.today()
    start = end - timedelta(days=comp_factor*period)

    df = pdr.get_data_yahoo(ticker, start=start, end=end)

    # cum_sums = {}
    #
    # for i in range(comp_factor*period, -1, -1):
    #     dt = end - timedelta(days=i)
    #     dt_str = dt.strftime('%Y-%m-%d')
    #     try:
    #         cum_sums[dt_str] = df.loc[dt_str].Close
    #     except KeyError as e:
    #         pass

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

    print("\n")
    if(num != 0):
        print("Moving average:            {:f}".format(tot/num))
        print("Current closing price:     {:f}".format(df.loc[end.strftime('%Y-%m-%d')].Close))
    time.sleep(5)
