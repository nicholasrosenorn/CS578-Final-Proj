#methods to add fields to data
#the data that is added requires access to all data, not just data of interest
#add: 
#   daily change %
#   22 day change %
#   44 day change %
#   66 day change %
#   volatility 
#   s and p day change %
#   beta 
#   1 year interest rate TODO NICK
#   pharmacutical labal TODO NICK
#   earnings per share TODO: note: this maybe should done after getting data of interest (ie: in generateMLData) JP


#in: none
#out: none
# methods get called by createdata.py

import pandas as pd
import numpy as np
import math


#column indexes
changeindex = 10
closeindex = 7
_22daychangeindex = 11
_44daychangeindex = 12
_66daychangeindex = 13
hvindex = 14
spycloseindex = 15
spyindex = 16
spyhvindex = 17
betaindex = 18
f22dayindex = 19
f44dayindex = 20
f66dayindex = 21
dateindex = 2


def addPercentChanges(df, length):
    df, length = removeColumns(df, length)
    df = calcDailyChange(df, length)
    df = calc22DayChange(df, length)
    df = calc44DayChange(df, length)
    df = calc66DayChange(df, length)
    df = calcVolatility(df, length)

    return df

def marketData(df, length, spy):
    df = spReturn(df, length, spy)
    df = calcBeta(df, length, spy)

    return df

def addOtherData(df, length):
    df = futurePrices(df, length)

    df = df.drop(columns = '<SPY_CLOSE>')

    return df
    

#removes columns that I dont think are needed, may be changed
#updates column indexs 
def removeColumns(df, length):
    todrop = ['<PER>', '<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<VOL>', '<OPENINT>']
    df = df.drop(columns = todrop)
    global changeindex, dateindex
    global closeindex
    global _22daychangeindex
    global _44daychangeindex
    global _66daychangeindex
    global hvindex
    global spycloseindex, spyindex
    global spyhvindex
    global betaindex, f22dayindex, f44dayindex, f66dayindex

    change = len(todrop)
    changeindex = 10 - change
    dateindex = 2- 1 #because only PER is removed in front of it
    closeindex = 7 - 5 #because others are appendend at end and it is not
    _22daychangeindex = 11- change
    _44daychangeindex = 12 - change
    _66daychangeindex = 13 - change
    hvindex = 14 - change
    spycloseindex = 15 - change
    spyindex = 16 - change
    spyhvindex = 17 - change
    betaindex = 18 - change
    f22dayindex = 19 - change
    f44dayindex = 20 - change
    f66dayindex = 21 - change


    #also trim length
    for i in range(0, length):
        if(df.iat[i, dateindex] > 20150101):
            break
    df = df[i:]

    length = len(df.index)
        
    return df, length
    

#finds the percent change from close yesterday to close today. 
#effectivly change over today
def calcDailyChange(df, length):
    df['<CHANGE>'] = "{:.4f}".format(0.0000)
    for i in range(1, length):
        df.iat[i, changeindex] = "{:.4f}".format((df.iat[i, closeindex] - df.iat[i-1, closeindex]) / df.iat[i-1, closeindex] * 100)

    return df

#finds 22 weekday percent return
def calc22DayChange(df, length):
    df['<22Day>'] = "{:.4f}".format(0.0000)
    for i in range(22, length):
        df.iat[i, _22daychangeindex] = "{:.4f}".format((df.iat[i, closeindex] - df.iat[i-22, closeindex]) / df.iat[i-22, closeindex] * 100)

    return df 

#finds 44 day percent return
def calc44DayChange(df, length):
    df['<44Day>'] = "{:.4f}".format(0.0000)
    for i in range(44, length):
        df.iat[i, _44daychangeindex] = "{:.4f}".format((df.iat[i, closeindex] - df.iat[i-44, closeindex]) / df.iat[i-44, closeindex] * 100)

    return df

#finds 66 day percent return
def calc66DayChange(df, length):
    df['<66Day>'] = "{:.4f}".format(0.0000)
    for i in range(66, length):
        df.iat[i, _66daychangeindex] = "{:.4f}".format((df.iat[i, closeindex] - df.iat[i-66, closeindex]) / df.iat[i-66, closeindex] * 100)

    return df


def futurePrices(df, length):
    df['<F_22Day>'] = "{:.2f}".format(0.00)
    df['<F_44Day>'] = "{:.2f}".format(0.00)
    df['<F_66Day>'] = "{:.2f}".format(0.00)
    for i in range(0, length-22):
        df.iat[i, f22dayindex] = df.iat[i+22, closeindex]

    for i in range(0, length-44):
        df.iat[i, f44dayindex] = df.iat[i+44, closeindex]
    
    for i in range(0, length-66):
        df.iat[i, f66dayindex] = df.iat[i+66, closeindex]

    return df


#caluclates volatility over last 22 days (b/c VIX is 30 days)
# and then annualizes it
#SOA version of volatility for lognormal stock model
def calcVolatility(df, length):
    df['<HV>'] = "{:.4f}".format(0.0000)
    justclose = df.iloc[:, closeindex: closeindex+1].to_numpy()
    justclose = justclose.astype(float)
    log_change = list()
    for i in range(1, length):
        log_change.append(math.log(justclose[i] / justclose[i-1]))
    for i in range(23, length):
        variance = np.var(log_change[i-23:i], ddof = 1)
        df.iat[i, hvindex] = "{:.4f}".format(math.sqrt(variance * 365))

    return df



#calculates covariance between market and stock
#done over whole period
#use varaince of spy over whole period
def calcBeta(df, length, spy):
    #stock_change = df.iloc[:, closeindex : closeindex+1].to_numpy()
    #spy_change = df.iloc[:, spycloseindex : spycloseindex+1].to_numpy()
    #spyhv = df.iloc[:, spyhvindex : spyhvindex+1].to_numpy()
    
    #stock_change = stock_change.astype(float)
    #spy_change = spy_change.astype(float)
    #spyhv = spyhv.astype(float)

    #keeping this here in case I need it
    """
    log_stock = list()
    log_spy = list()
    for i in range(1, length):
        log_stock.append(math.log(stock_change[i] / stock_change[i-1]))
    
        log_spy.append(math.log(spy_change[i] / spy_change[i-1]))

    spy_var = np.var(log_spy, ddof = 1)
    covariance = np.cov(log_stock, log_spy)


    print(covariance)
    print(spy_var)
    print(spy_var * math.sqrt(365))
    print(np.var(log_stock) * math.sqrt(365),  math.sqrt(np.var(log_stock) )* math.sqrt(365))

        """

    stock_changep = df.iloc[:, changeindex : changeindex+1].to_numpy()
    spy_changep = df.iloc[:, spyindex : spyindex+1].to_numpy()
    stock_changep = stock_changep.astype(float)
    spy_changep = spy_changep.astype(float)

    spy_var = np.var(spy_changep)
    covariance = np.cov(spy_changep.T, stock_changep.T)



    df['<BETA>'] = "{:.4f}".format(covariance[1,0] / spy_var )
    return df


#attaches daily return of S&P to the stock at each date
def spReturn(df, length, spy):
    df = df.merge(spy, on = '<DATE>', how = 'left')
    todrop = ['<TICKER>_y', '<22Day>_y', '<44Day>_y', '<66Day>_y']
    df = df.drop(columns = todrop)
    df = df.rename(columns = {'<TICKER>_x' : '<TICKER>',
                              '<CLOSE>_x' : '<CLOSE>',
                              '<CHANGE>_x' : '<CHANGE>',
                              '<22Day>_x' : '<22Day>',
                              '<44Day>_x' : '<44Day>',
                              '<66Day>_x' : '<66Day>',
                              '<HV>_x' : '<HV>',
                              '<CLOSE>_y' : '<SPY_CLOSE>',
                              '<CHANGE>_y' : '<SPY_CHANGE>',
                              '<HV>_y' : '<SPY_HV>'})

    return df

#TODO
#label if compnay is a pharmacutical company
#def pharmIndustry():

#TODO
#attaches return of 1 year T-bill to each date
#def riskFreeReturn():


#TODO
#attaches earnings per share
#might be kinda hard, not sure. using yahoo finance api could work
#could do this step once we seperate out data points of interest (ie: in generateMLData.py)
#def earningsPerShare():


