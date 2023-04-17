# runs the logistical regression
# uses methods on generateMLData.py to get run specific data
#can adjust hyper parameters

#in: combined file of all data
#out: results of logistic regression, form TBD

import pandas as pd
import GenerateMLData

#This is all data in one file
inputfile = r"C:\Users\imhun\Documents\CS 578\Project\Data set\Development Dataset\output\combined.txt" 


#hyperparameters:
strikepercentage = .9   #percentage of stock price to strike price
daystoexpire = 22       #should be 22, 44, or 66

#model parameters
pricemodel = 0          #0 = european, 1 = american perpetual v1, 2 = american perpertual v2
profitformula = 1       #1 = profit at expiration

#selection criteria
minstockprice = 15      #minimum stock price to be selected
minstockgain = 10       #minimum percent daily change to be selected



def preparedata():
    df = pd.read_csv(inputfile, sep="\t")
    df = GenerateMLData.selectData(df, minstockprice, minstockgain)

    df = GenerateMLData.calcProfit(df, strikepercentage, daystoexpire, pricemodel, profitformula)
    print(df)

    return df
   
preparedata()
print("DONE PREPARE DATA")


#TODO JP
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


    
    

    