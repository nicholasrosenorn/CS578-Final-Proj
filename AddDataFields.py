#methods to add fields to data

import pandas as pd


#column indexes
changeindex = 10
closeindex = 7
_30daychangeindex = 11
_60daychangeindex = 12
_90daychangeindex = 13


def addAll(df, length):
    calcDailyChange(df, length)
    calc30DayChange(df, length)
    calc60DayChange(df, length)
    calc90DayChange(df, length)

#finds the change from close yesterday to close today. 
#effectivly change over today
def calcDailyChange(df, length):
    df['<CHANGE>'] = 0 
    for i in range(1, length):
        df.iat[i, changeindex] = (df.iat[i, closeindex] - df.iat[i-1, closeindex]) / df.iat[i-1, closeindex]


#finds 30 day return
def calc30DayChange(df, length):
    df['<30Day>'] = 0 
    for i in range(30, length):
        df.iat[i, _30daychangeindex] = (df.iat[i, closeindex] - df.iat[i-30, closeindex]) / df.iat[i-30, closeindex]

#finds 60 day return
def calc60DayChange(df, length):
    df['<60Day>'] = 0 
    for i in range(60, length):
        df.iat[i, _60daychangeindex] = (df.iat[i, closeindex] - df.iat[i-60, closeindex]) / df.iat[i-60, closeindex]

#finds 90 day return
def calc90DayChange(df, length):
    df['<90Day>'] = 0 
    for i in range(90, length):
        df.iat[i, _90daychangeindex] = (df.iat[i, closeindex] - df.iat[i-90, closeindex]) / df.iat[i-90, closeindex]


#def calcVolatility():


#def calcBeta():


    