import pandas as pd
import csv

mid_type = ''

def cal_mid_price (gr_bid_level, gr_ask_level): 

    level = 5
    #gr_rB = gr_bid_level.head(level)
    #gr_rT = gr_ask_level.head(level)

    if len(gr_bid_level) > 0 and len(gr_ask_level) > 0:
        bid_top_price = gr_bid_level.iloc[0].price
        bid_top_level_qty = gr_bid_level.iloc[0].quantity
        ask_top_price = gr_ask_level.iloc[0].price
        ask_top_level_qty = gr_ask_level.iloc[0].quantity
        mid_price = (bid_top_price + ask_top_price) * 0.5 #what is mid price?

        return (mid_price)

    else:
        print ('Error: serious cal_mid_price')
        return (-1)
    

def live_cal_book_i_v1(param, gr_bid_level, gr_ask_level, mid):
    
    mid_price = mid

    ratio = param[0]; level = param[1]; interval = param[2]
    #print ('processing... %s %s,level:%s,interval:%s' % (sys._getframe().f_code.co_name,ratio,level,interval)), 
    

    quant_v_bid = gr_bid_level.quantity**ratio
    price_v_bid = gr_bid_level.price * quant_v_bid

    quant_v_ask = gr_ask_level.quantity**ratio
    price_v_ask = gr_ask_level.price * quant_v_ask
 
    #quant_v_bid = gr_r[(gr_r['type']==0)].quantity**ratio
    #price_v_bid = gr_r[(gr_r['type']==0)].price * quant_v_bid

    #quant_v_ask = gr_r[(gr_r['type']==1)].quantity**ratio
    #price_v_ask = gr_r[(gr_r['type']==1)].price * quant_v_ask
        
    askQty = quant_v_ask.values.sum()
    bidPx = price_v_bid.values.sum()
    bidQty = quant_v_bid.values.sum()
    askPx = price_v_ask.values.sum()
    bid_ask_spread = interval
        
    book_price = 0 #because of warning, divisible by 0
    if bidQty > 0 and askQty > 0:
        book_price = (((askQty*bidPx)/bidQty) + ((bidQty*askPx)/askQty)) / (bidQty+askQty)

        
    indicator_value = (book_price - mid_price) / bid_ask_spread
    #indicator_value = (book_price - mid_price)
    
    return indicator_value


df = pd.read_csv('2023-11-15-upbit-BTC-book.csv').apply(pd.to_numeric,errors='ignore')
groups = df.groupby('timestamp')

keys = groups.groups.keys()

filename = '2023-11-15-upbit-BTC-feature.csv'

with open(filename, 'w') as csvfile:
    csv_header ='book-imbalance-0.2-5-1, mid_price, timestamp\n'
    csvfile.write(csv_header)
    
    for i in keys:
        gr_o = groups.get_group(i)
        gr_bid_level = gr_o[(gr_o.type == 0)].head(5)
        gr_ask_level = gr_o[(gr_o.type == 1)].head(5)
        mid_p = cal_mid_price(gr_bid_level,gr_ask_level)
        book_i = live_cal_book_i_v1((0.2,5,1), gr_bid_level, gr_ask_level, mid_p)
        time = i
        csvfile.write(f'{book_i},{mid_p},{time}\n')
       
    
     