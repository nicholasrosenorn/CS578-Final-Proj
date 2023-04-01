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
#   1 year interest rate TODO
#   pharmacutical labal TODO
#   earnings per share TODO: note: this maybe should done after getting data of interest (ie: in generateMLData)


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
spyindex = 15
spyhvindex = 16
betaindex = 17
f22dayindex = 18
f44dayindex = 19
f66dayindex = 20
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
    global spyindex
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
    spyindex = 15 - change
    spyhvindex = 16 - change
    betaindex = 17 - change
    f22dayindex = 18 - change
    f44dayindex = 19 - change
    f66dayindex = 20 - change


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
# assume 252 trading days in a year
def calcVolatility(df, length):
    df['<HV>'] = "{:.4f}".format(0.0000)
    justHV = df.iloc[:, changeindex: changeindex+1].to_numpy()
    justHV = justHV.astype(float)
    for i in range(23, length):
        variance = np.var(justHV[i-23:i])
        df.iat[i, hvindex] = "{:.4f}".format(math.sqrt(variance * 252))

    return df


#TODO: check math, im very sure it is wrong
#calculates covariance between market and stock
#done over whole period
#use varaince of spy over whole period
def calcBeta(df, length, spy):
    hv = df.iloc[:, hvindex : hvindex+1].to_numpy()
    spyhv = df.iloc[:, spyhvindex : spyhvindex+1].to_numpy()
    hv = hv.astype(float)
    spyhv = spyhv.astype(float)
    covariance = np.cov(hv.T, spyhv.T)

    spychange= df.iloc[:, spyindex: spyindex+1].to_numpy()
    spychange = spychange.astype(float)
    variance = np.var(spychange)

    df['<BETA>'] = "{:.4f}".format(covariance[1,0] / variance)
    return df


#attaches daily return of S&P to the stock at each date
def spReturn(df, length, spy):
    df = df.merge(spy, on = '<DATE>', how = 'left')
    todrop = ['<TICKER>_y', '<CLOSE>_y', '<22Day>_y', '<44Day>_y', '<66Day>_y']
    df = df.drop(columns = todrop)
    df = df.rename(columns = {'<TICKER>_x' : '<TICKER>',
                              '<CLOSE>_x' : '<CLOSE>',
                              '<CHANGE>_x' : '<CHANGE>',
                              '<22Day>_x' : '<22Day>',
                              '<44Day>_x' : '<44Day>',
                              '<66Day>_x' : '<66Day>',
                              '<HV>_x' : '<HV>',
                              '<CHANGE>_y' : '<SPY>',
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


