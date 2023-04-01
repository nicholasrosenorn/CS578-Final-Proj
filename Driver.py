# runs the logistical regression
# uses methods on generateMLData.py to get run specific data
#can adjust hyper parameters

#in: combined file of all data
#out: results of logistic regression, form TBD

import pandas as pd
import GenerateMLData

#This is all data in one file
inputfile = r"C:\Users\imhun\Documents\CS 578\Project\Data set\Development Dataset\combined.txt" 


#hyperparameters:
strikepercentage = .9   #percentage of stock price to strike price
daystoexpire = 22       #should be 22, 44, or 66

#model parameters
american = True         #true for american perpetual, false for european
profitformula = 1       #1 = profit at expiration

#selection criteria
minstockprice = 15      #minimum stock price to be selected
minstockgain = 10       #minimum percent daily change to be selected



def preparedata():
    df = pd.read_csv(inputfile, sep="\t")

    df = GenerateMLData.selectData(df, minstockprice, minstockgain)

    df = GenerateMLData.calcProfit(df, strikepercentage, daystoexpire, american, profitformula)

    return df
   
#TODO
#may reorganize structure
# do we need to code own or can use sklearn?
def learnAlgorithm():
    df = preparedata()

    # seperate into training, testing, and validation
    trainSet = df.sample(frac = .8)
    rest20 = df.drop(trainSet.index)
    validateSet = rest20.sample(frac = .5)
    testSet = rest20.drop(validateSet.index)

    
    #run logistic regression


    
    

    