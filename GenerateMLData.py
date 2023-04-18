##methods to add fields to data
#the data that is added only requires data of interest
#add: 
#   Select Data
#   European put price 
#   American perpetual put price (two versions)
#   Calc Profit
#   

#in: none
#out: none

#methods are called by driver.py

import pandas as pd
from scipy.stats import norm
import math
import TickerLabels


#column indexes
tickerindex = 0
dateindex = 1
closeindex = 2
changeindex = 3
_22daychangeindex = 4
_44daychangeindex = 5
_66daychangeindex = 6
hvindex = 7
spychangeindex = 8
spyhvindex = 9
betaindex = 10
f22dayindex = 11
f44dayindex = 12
f66dayindex = 13
interestindex = 14
"""
sectorindex = 15
industryindex = 16

optionpriceindex = 17
profitindex = 18
labelindex = 19
"""

optionpriceindex = 15
profitindex = 16
labelindex = 17

#TODO check work
#selects data based on minimum criteria
def selectData(df, stockprice, stockpercentage):
    # if price > stockprice and change > stockpercentage then add
    #for i in range(0, len(df.index)):
        #if(df.iat[i, closeindex] < stockprice or df.iat[i, changeindex] < stockpercentage):
        #    df.drop(i)
    df = df[df['<CHANGE>'] > stockpercentage]
    df = df[df['<CLOSE>'] > stockprice]

    #df = TickerLabels.join_labels_combined(df)
    

    return df

#TODO check work
def calcProfit(df, strikepercentage, daystoexpire, pricemodel, profitformula):    
    
    match profitformula:
        case 1:
            #new column is max[(strike - stockprice), 0]  - option cost
            #new column is ^ > 0 then 1 else 0

            match daystoexpire:
                case 22:
                    daysindex = f22dayindex
                case 44:
                    daysindex = f44dayindex
                case 66:
                    daysindex = f66dayindex


            match pricemodel:

                case 0:
                    df = european(df, strikepercentage, daystoexpire)
                case 1:
                    df = american1(df, strikepercentage, daystoexpire)
                case 2:
                    df = american2(df, strikepercentage, daystoexpire)

            df['<PROFIT>'] = "{:.2f}".format(0.00)
            df['<LABEL>'] = 0

            for i in range(0, len(df.index)):
                df.iat[i, profitindex] = float("{:.2f}".format(max(df.iat[i, closeindex] * strikepercentage - df.iat[i, daysindex], 0) - df.iat[i, optionpriceindex]))

                if(df.iat[i, profitindex] > 0):
                    df.iat[i, labelindex] = 1

                
            
    return df


#calculates the price of a european option
def european(df, strikepercentage, daystoexpire):
    t = daystoexpire / 365

    df['<PRICE>'] = "{:.2f}".format(0.00)

    for i in range(0, len(df.index)):
        p = df.iat[i, closeindex] #stock price
        k = strikepercentage * p #strike value
        r = df.iat[i, interestindex ] / 100 #interest rate, given as percentage
        sd = df.iat[i, hvindex] #volatility
        
        d1 = (math.log(1/strikepercentage) + (r+(sd**2)/2)*t) / (sd*math.sqrt(t))
        d2 = d1 - sd*math.sqrt(t)

        price = norm.cdf(-d2)*k*math.exp(-r*t) - norm.cdf(-d1)*p

        df.iat[i, optionpriceindex] = float("{:.2f}".format(price))



    return df


# add formula for american perpetual put
#formula from http://www.stat.uchicago.edu/~lalley/Courses/391/Lecture15.pdf
def american1(df, strikepercentage, daystoexpire):

    df['<PRICE>'] = "{:.2f}".format(0.00)

    for i in range(0, len(df.index)):
        p = df.iat[i, closeindex] #stock price
        k = strikepercentage * p #strike value
        r = df.iat[i, interestindex ] / 100 #interest rate, given as percentage
        sd = df.iat[i, hvindex] #volatility


        price = k * (k / p * (1 - 2*r / (2*r + sd**2) ) ) ** (2*r / (sd **2) )
        df.iat[i, optionpriceindex] = float("{:.2f}".format(price))
    return df


# add formula for american perpetual put
#formula from https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
# and https://web.ma.utexas.edu/users/mcudina/Lecture14_1and2.pdf
#assumes no dividend
def american2(df, strikepercentage, daystoexpire):

    df['<PRICE>'] = "{:.2f}".format(0.00)

    for i in range(0, len(df.index)):
        p = df.iat[i, closeindex] #stock price
        k = strikepercentage * p #strike value
        r = df.iat[i, interestindex ] / 100 #interest rate, given as percentage
        sd = df.iat[i, hvindex] #volatility
        var = sd ** 2

        h1 = ( - (r - .5 * var) + math.sqrt((r - .5 * var) ** 2 + 2*var*r) ) / var
        h2 = ( - (r - .5 * var) - math.sqrt((r - .5 * var) ** 2 + 2*var*r) ) / var
        
        price = k / (1 - h2) * ((h2 - 1) / h2 * (p / k)) ** h2 

        df.iat[i, optionpriceindex] = float("{:.2f}".format(price))
    return df