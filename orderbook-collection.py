import time
import requests
import pandas as pd
from datetime import datetime
import csv

n=1

while True:
    book ={}
    response =requests.get('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()

    data = book['data']

    bids = pd.DataFrame(data['bids']).apply(pd.to_numeric, errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids.reset_index(drop=True, inplace=True)
    bids['type'] = 0

    asks = pd.DataFrame(data['asks']).apply(pd.to_numeric, errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks.reset_index(drop=True, inplace=True)
    asks['type'] = 1

    df = pd.concat([bids, asks], ignore_index=True)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    df['timestamp'] = current_time
    result = df['price'].astype(str) + ' | ' + df['quantity'].astype(str) + ' | ' + df['type'].astype(str) + ' | ' + df['timestamp']
    results =result.to_string(index=False)

    if n==1:
        header='price         |quantity|type|timestamp'
        print(header)
        with open('output.csv', 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(header)

        n = n + 1


    print(results)

    with open('output.csv', 'a', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(results.split())

    time.sleep(3)
