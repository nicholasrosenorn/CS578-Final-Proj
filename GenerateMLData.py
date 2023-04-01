##methods to add fields to data
#the data that is added only requires data of interest
#add: 
#   Select Data
#   European put price 
#   American perpetual put price TODO IAN
#   Calc Profit
#   

#in: none
#out: none

#methods are called by driver.py

import pandas as pd
from scipy.stats import norm
import math



#TODO check work
#selects data based on minimum criteria
def selectData(df, stockprice, stockpercentage):
    # if price > stockprice and change > stockpercentage then add

    for i in range(0, len(df.index)):
        if(df[i, 2] < stockprice or df[i, 3] < stockpercentage):
            df.drop(i)

    return df

#TODO check work
def calcProfit(df, strikepercentage, daystoexpire, american, profitformula):    
    
    match profitformula:
        case 1:
            #new column is max[(strike - stockprice), 0]  - option cost
            #new column is ^ > 0 then 1 else 0

            match daystoexpire:
                case 22:
                    daysindex = 11
                case 44:
                    daysindex = 12
                case 66:
                    daysindex = 13

            if(american):
                df = american(df, strikepercentage, daystoexpire)
                #TODO
                return df
            else:
                df = european(df, strikepercentage, daystoexpire)
                

                length = len(df.columns)
                df['<PROFIT>'] = "{:.2f}".format(0.00)
                df['<LABEL>'] = 0

                for i in range(0, len(df.index)):
                    df[i, length] = max(df[i, 2] * strikepercentage - df[i, daysindex], 0) - df[i, length -1]

                    if(df[i, length] > 0):
                        df[length + 1] = 1

                return df
            
            
    return df


#TODO check math
def european(df, strikepercentage, daystoexpire):
    t = daystoexpire

    length = len(df.columns)
    df['<PRICE>'] = "{:.2f}".format(0.00)

    for i in range(0, len(df.index)):
        p = df.iat[i, 2] #stock price
        k = strikepercentage * p #will be stock price
        r = 1 #interest rate
        sd = df.iat[i, 7] #volatility
        

        d1 = (math.log(1/strikepercentage) + (r+(sd**2)/2)*t) / (sd*math.sqrt(t))
        d2 = d1 - sd*math.sqrt(t)

        price = norm.cdf(-d2)*k*math.exp(-r*t) - norm.cdf(-d1)*p
        df[i, length] = price



    return df

#TODO
# add formula for american perpetual put
def american(df, strikepercentage, daystoexpire):

    return df