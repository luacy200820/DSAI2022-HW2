import pandas as pd 
import numpy as np 

import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt 
import datetime,time
# You can write code above the if-main block.

K = D = 0

## Calculate Bollinger Bands
def bbands(tsPrice,period=20,times=2):
    upBBand=pd.Series(0.0,index=tsPrice.index)
    midBBand=pd.Series(0.0,index=tsPrice.index)
    downBBand=pd.Series(0.0,index=tsPrice.index)
    sigma=pd.Series(0.0,index=tsPrice.index)
    for i in range(period-1,len(tsPrice)):
        midBBand[i]=np.nanmean(tsPrice[i-(period-1):(i+1)])
        sigma[i]=np.nanstd(tsPrice[i-(period-1):(i+1)])
        upBBand[i]=midBBand[i]+times*sigma[i]
        downBBand[i]=midBBand[i]-times*sigma[i]
    BBands=pd.DataFrame({'upBBand':upBBand[(period-1):],\
                         'midBBand':midBBand[(period-1):],\
                         'downBBand':downBBand[(period-1):],\
                         'sigma':sigma[(period-1):]})
    return(BBands)

# plot stock chart
def plot_bb(data,bb):

    gs = gridspec.GridSpec(2, 1, left=0.08, bottom=0.15, right=0.99, top=0.96, wspace=None, hspace=0, height_ratios=[2.5,1])
    fig = plt.figure(figsize=(20,9), dpi=100,facecolor="white") #創建fig對象

    graph_KAV = fig.add_subplot(gs[1,:])

    graph_bb = fig.add_subplot(gs[0,:])

    data_len = len(bb.downBBand)
    # plt.figure(figsize=(20,12))

    graph_bb.plot(data['close'],label="Close",color='k',marker='d')
    graph_bb.plot(data['open'],label="open",color='g',marker='2')
    # graph_bb.rcParams['font.sans-serif'] = ['simhei']
    graph_bb.plot(bb.upBBand,
            label="upBBand",color='b',marker='o',
            linestyle='dashed')
    graph_bb.plot(data['ma'],
            label="10ma",color='y',marker='d',
            linestyle='dashed')
    graph_bb.plot(data['ma5'],
            label="5ma",color='c',marker='x',
            linestyle='dashed')
    graph_bb.plot(bb.midBBand,
            label="midBBand",color='r',linestyle='-.',marker='o')
    graph_bb.plot(bb.downBBand,
            label="downBBand",color='b',marker='o',
            linestyle='dashed')

    graph_bb.legend(loc='best')    
    graph_bb.set_ylabel("stock")


    graph_KAV.plot(data['RSV'],label="RSV",color='r',marker='x',linestyle='-.')
    graph_KAV.plot(data['K'],label="K",color='k',marker='d')
    graph_KAV.plot(data['D'],label="D",color='g',marker='o')
    graph_KAV.legend(loc='best')    
    graph_KAV.set_ylabel("KDR")

    plt.show()  

# Set date range 
def make_date(day_len):
    d1 = datetime.datetime.now()
    d3 = d1 - datetime.timedelta(days=day_len)
    d3.ctime()
    past_time = d3.strftime("%Y %m %d")
    now_time = d1.strftime("%Y %m %d")
    date_print=pd.date_range(start=past_time,end=now_time)
    return date_print

def Kvalue(rsv):
    global K
    K = (2/3) * K + (1/3) * rsv
    return K

def Dvalue(k):
    global D
    D = (2/3) * D + (1/3)*k
    return D

# Calcuate MACD color 
def macd_color(r):
    return 'red' if r["OSC"] > 0 else 'green'



def stock_action2( old_data,new_data,past_action,cost_money):
  
    old_data = old_data.append(new_data,ignore_index=True)
    date_data = make_date(len(old_data)-1)

    time_datest_df=pd.DataFrame(old_data,columns=['open','high','low','close'])
    time_datest_df['date'] = date_data

    result = time_datest_df.set_index('date')

    bbresult = bbands(result,20,2)
    
    ma10 = result["close"].rolling("10D").mean()
    result['ma'] = ma10
    ma5 = result["close"].rolling("5D").mean()
    result['ma5'] = ma5


    result['exp12'] = result['close'].ewm(span=12,adjust = False).mean()
    result['exp26'] = result['close'].ewm(span = 26,adjust=False).mean()
    result['DIF'] = result['exp12'] - result['exp26']
    result["DEM"] = result['DIF'].ewm(span=9, adjust=False).mean()
    result['OSC'] = 2*(result['DIF'] - result['DEM'])

    ##RSV
    result['9DAYMAX'] = result['high'].rolling('9D').max()
    result['9DAYMIN'] = result['low'].rolling('9D').min()

    result['RSV'] = 0 
    result['RSV'] = 100 * (result['close'] - result['9DAYMIN']) / (result['9DAYMAX'] - result['9DAYMIN'])

    ##KD value
    K = 0
    result['K'] = 0
    result['K'] = result['RSV'].apply(Kvalue)

    D = 0
    result['D']=0
    result['D'] = result['K'].apply(Dvalue)

    result['macd_color'] = result.apply(macd_color, axis=1) 
    # plot_bb(result,bbresult)

    # Judging buying and selling actions
    if past_action == 0 and result.iloc[-1]['RSV'] > 85 :
        action = -1 
    elif past_action == 1 and result.iloc[-1]['RSV'] > 85:
        action = -1
    elif past_action == 0 and result.iloc[-1]['RSV'] < 15 :
        action = 1
    elif past_action == -1 and result.iloc[-1]['RSV'] < 15 :
        action = 1 
    elif past_action == 0 and result.iloc[-1]['close'] > bbresult.upBBand[-1] and result.iloc[-2]['close'] < bbresult.upBBand[-2] :
        action = 0 #假突破，不做事
    # elif past_action == 0 and result.iloc[-1]['close'] < bbresult.upBBand[-1] and result.iloc[-2]['close'] > bbresult.upBBand[-2] :
        # action = 0 #假突破，不做事
    elif past_action == 0 and result.iloc[-1]["close"] > bbresult.upBBand[-1] :
        action = -1
    elif past_action == 0 and (result.iloc[-1]["close"] < bbresult.downBBand[-1]):
        action = 1 
    elif past_action == 0 and ma5[-1] <= bbresult.midBBand[-1] and ma5[-2] > bbresult.midBBand[-2] :
        action = -1
    elif past_action == 0 and ma5[-1] > bbresult.midBBand[-1] and ma5[-2] <= bbresult.midBBand[-2]:
        action = 1
    elif past_action == 0 and result.iloc[-1]['D'] < 10 :
        action = 1
    elif past_action == 0 and result.iloc[-1]['K'] > 90 :
        action = -1

    elif past_action == -1 and result.iloc[-1]['D'] < 10 :
        action = 1
    elif past_action == 1 and result.iloc[-1]['K'] > 90 :
        action = -1

    elif past_action == 1 and result.iloc[-1]['K'] > 85 and result.iloc[-1]['D'] >75:
        action = -1
    elif past_action == -1 and result.iloc[-1]['K'] < 15 and result.iloc[-1]['D'] <25:
        action = 1 
    elif past_action == -1 and cost_money < result.iloc[-1]['close'] and cost_money < result.iloc[-3]['close'] and  cost_money < result.iloc[-3]['close']:
        action = 1 # 停損
    elif past_action == 1 and cost_money > result.iloc[-1]['close'] and cost_money > result.iloc[-3]['close'] and  cost_money > result.iloc[-3]['close']:
        action = -1 # 停損
    elif past_action == -1 and ma5[-1] < bbresult.midBBand[-1] and ma5[-2] < bbresult.midBBand[-2] and ma5[-3] < bbresult.midBBand[-3]:
        action = 1
    elif past_action == 1 and ma5[-1] > bbresult.midBBand[-1] and ma5[-2] > bbresult.midBBand[-2] and ma5[-3] > bbresult.midBBand[-3]:
        action = -1
    elif past_action == -1 and result.iloc[-1]['close'] >= bbresult.upBBand[-1] and result.iloc[-2]['close'] >= bbresult.upBBand[-2] and result.iloc[-3]['close'] >= bbresult.upBBand[-3]:
        action = 1 # 放空停損
    elif past_action == 1 and result.iloc[-1]['close'] <= bbresult.downBBand[-1] and result.iloc[-2]['close'] <= bbresult.downBBand[-2] and result.iloc[-3]['close'] <= bbresult.downBBand[-3]:
        action = -1 # 看多停損  
  

    else :
        action=0

    past_action = int(past_action) + int(action)

    return old_data,past_action,action

if __name__ == '__main__':
    # You should not modify this part.
    import argparse


    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
    args = parser.parse_args()
    
    # The following part is an example.
    # You can modify it at will.
    training_data = pd.read_csv(args.training,header=None)
    training_data.columns = ['open','high','low','close']
    data = training_data.copy()

    
    testing_data = pd.read_csv(args.testing,header=None)
    testing_data.columns = ['open','high','low','close']

    action = 0
    cost = 0
    buy = 0
    sell = 0 
    profit = 0
    answer = 0 
    stock_action = []
    with open(args.output, 'w') as output_file:
        for row in range(len(testing_data)):
            if answer == -1 :
                sell = testing_data.iloc[row]['open']
                cost = sell

            elif answer == 1 :
                buy = testing_data.iloc[row]['open']
                cost = buy
  
            if action == 0 and answer != 0:
                profit = profit+(sell -buy) 
                cost = 0         
            if row != 19:
                data,action,answer = stock_action2(data,testing_data.iloc[row],action,cost)

                output_file.write(str(answer)+'\n')

