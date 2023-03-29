#methods to add fields to data

import pandas as pd


#column indexes
changeindex = 10
closeindex = 7
_22daychangeindex = 11
_44daychangeindex = 12
_66daychangeindex = 13


def addAll(df, length):
    calcDailyChange(df, length)
    calc22DayChange(df, length)
    calc44DayChange(df, length)
    calc66DayChange(df, length)

#finds the change from close yesterday to close today. 
#effectivly change over today
def calcDailyChange(df, length):
    df['<CHANGE>'] = "{:.4f}".format(0.000)
    for i in range(1, length):
        df.iat[i, changeindex] = "{:.4f}".format((df.iat[i, closeindex] - df.iat[i-1, closeindex]) / df.iat[i-1, closeindex])


#finds 22 weekday return
def calc22DayChange(df, length):
    df['<22Day>'] = "{:.4f}".format(0.000)
    for i in range(22, length):
        df.iat[i, _22daychangeindex] = "{:.4f}".format((df.iat[i, closeindex] - df.iat[i-22, closeindex]) / df.iat[i-22, closeindex])

#finds 60 day return
def calc44DayChange(df, length):
    df['<44Day>'] = "{:.4f}".format(0.000)
    for i in range(44, length):
        df.iat[i, _44daychangeindex] = "{:.4f}".format((df.iat[i, closeindex] - df.iat[i-44, closeindex]) / df.iat[i-44, closeindex])

#finds 90 day return
def calc66DayChange(df, length):
    df['<66Day>'] = "{:.4f}".format(0.000)
    for i in range(66, length):
        df.iat[i, _66daychangeindex] = "{:.4f}".format((df.iat[i, closeindex] - df.iat[i-66, closeindex]) / df.iat[i-66, closeindex])



#def calcVolatility():

#def calcBeta():

#def spReturn():

#def pharmIndustry():




    