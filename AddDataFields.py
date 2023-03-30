#methods to add fields to data

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


def addAll(df, length):
    df = removeColumns(df, length)
    #print(df)
    df = calcDailyChange(df, length)
    df = calc22DayChange(df, length)
    df = calc44DayChange(df, length)
    df = calc66DayChange(df, length)
    df = calcVolatility(df, length)

    return df

def market(df, length, spy):
    df = spReturn(df, length, spy)
    df = calcBeta(df, length, spy)

    return df


#removes columns that I dont think are needed, may be changed
#updates column indexs 
def removeColumns(df, length):
    todrop = ['<PER>', '<TIME>', '<OPEN>', '<HIGH>', '<LOW>', '<VOL>', '<OPENINT>']
    df = df.drop(columns = todrop)
    global changeindex 
    global closeindex
    global _22daychangeindex
    global _44daychangeindex
    global _66daychangeindex
    global hvindex
    global spyindex
    global spyhvindex
    global betaindex

    change = len(todrop)
    changeindex = 10 - change
    closeindex = 7 - 5 #because others are appendend at end and it is not
    _22daychangeindex = 11- change
    _44daychangeindex = 12 - change
    _66daychangeindex = 13 - change
    hvindex = 14 - change
    spyindex = 15 - change
    spyhvindex = 16 - change
    betaindex = 17 - change
    
    return df
    

#finds the percent change from close yesterday to close today. 
#effectivly change over today
def calcDailyChange(df, length):
    df['<CHANGE>'] = "{:.4f}".format(0.000)
    #print(changeindex)
    #print(closeindex)
    #print(type(df.iat[1, changeindex]))
    #print(type(df.iat[1, closeindex]))
    #print(df.iat[1, changeindex])
    #print(df.iat[1, closeindex])
    for i in range(1, length):
        df.iat[i, changeindex] = "{:.4f}".format((df.iat[i, closeindex] - df.iat[i-1, closeindex]) / df.iat[i-1, closeindex] * 100)

    return df

#finds 22 weekday percent return
def calc22DayChange(df, length):
    df['<22Day>'] = "{:.4f}".format(0.000)
    for i in range(22, length):
        df.iat[i, _22daychangeindex] = "{:.4f}".format((df.iat[i, closeindex] - df.iat[i-22, closeindex]) / df.iat[i-22, closeindex] * 100)

    return df 

#finds 60 day percent return
def calc44DayChange(df, length):
    df['<44Day>'] = "{:.4f}".format(0.000)
    for i in range(44, length):
        df.iat[i, _44daychangeindex] = "{:.4f}".format((df.iat[i, closeindex] - df.iat[i-44, closeindex]) / df.iat[i-44, closeindex] * 100)

    return df

#finds 90 day percent return
def calc66DayChange(df, length):
    df['<66Day>'] = "{:.4f}".format(0.000)
    for i in range(66, length):
        df.iat[i, _66daychangeindex] = "{:.4f}".format((df.iat[i, closeindex] - df.iat[i-66, closeindex]) / df.iat[i-66, closeindex] * 100)

    return df


#caluclates volatility over last 22 days (b/c VIX is 30 days)
# and then annualizes it
# assume 252 trading days in a year
def calcVolatility(df, length):
    df['<HV>'] = "{:.4f}".format(0.000)
    justHV = df.iloc[:, changeindex: changeindex+1].to_numpy()
    #print(bitches)
    justHV = justHV.astype(float)
    #print(bitches)
    for i in range(23, length):
        #print(type(bitches))
        #print(type(bitches[i-23:i]))
        #print(type(bitches[i:i+1]))
        
        variance = np.var(justHV[i-23:i])
        #print(variance)
        #print(i)
        #print(hvindex)
        df.iat[i, hvindex] = "{:.4f}".format(math.sqrt(variance * 252))

    return df


#TODO: check math
#calculates covariance between market and stock
#done over whole period
#use varaince of spy over whole period
def calcBeta(df, length, spy):
    hv = df.iloc[:, hvindex : hvindex+1].to_numpy()
    spyhv = df.iloc[:, spyhvindex : spyhvindex+1].to_numpy()
    print(hv[1:2])
    print(spyhv[1:2])
    hv = hv.astype(float)
    spyhv = spyhv.astype(float)
    covariance = np.cov(hv.T, spyhv.T)

    spychange= df.iloc[:, spyindex: spyindex+1].to_numpy()
    print(spychange[1:2])
    spychange = spychange.astype(float)
    variance = np.var(spychange)

    print(variance, covariance)
    print(covariance[1,0])

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
#could do this step once we seperate out data points of interest
#def earningsPerShare():


