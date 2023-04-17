#imports data and calls methods to add datafields
#import data is used to test methods
#import group data is method to use on whole data set when code is finialzed
#will return a full data set that can be analyzed for data of interest

#in: text files of stocks, s and p data, interest rates
#out: a full text file of concatenated stocks with added fields

import pandas as pd
import glob
import os
import AddDataFields

#data from https://stooq.com/db/h/ 
#U.S daily data
#folders are 
#d_us_txt.zip\data\daily\us\nasdaq stocks and
#d_us_txt.zip\data\daily\us\nyse stocks
# I put all ~5,000 text files into one folder

#I created a subset of 10 files to use for testing and developing

#paths to change for local use
folderpath = r"C:\Users\imhun\Documents\CS 578\Project\Data set\Development Dataset"
outputfile = r"C:\Users\imhun\Documents\CS 578\Project\Data set\Development Dataset\output\combined.txt"
singlefilepath = r"C:\Users\imhun\Documents\CS 578\Project\Data set\aapl.us.txt"
spyfilepath = r"C:\Users\imhun\Documents\CS 578\Project\Data set\spy.us.txt"



#using to test methods on single text files
def importdata():
    df = pd.read_csv(singlefilepath, sep=",")
    spy = pd.read_csv(spyfilepath, sep = ",")
    length = len(df.index)
    spylength = len(spy.index)
    df = df.round(2)
    spy = spy.round(2)

    df = AddDataFields.addPercentChanges(df, length)
    length = len(df.index)
    spy = AddDataFields.addPercentChanges(spy, spylength)
    df = AddDataFields.marketData(df, length, spy)
    df = AddDataFields.addOtherData(df, length)
    
    
    df.to_csv(r"C:\Users\imhun\Documents\CS 578\Project\Data set\aapl.us_test.txt", sep = '\t', index = False)
    




#importdata()
#print("DONE")


#using to test methods on group of text files
def importdatagroup():
    path = folderpath
    all_files = glob.glob(os.path.join(path , "*.txt"))

    li = []

    spy = pd.read_csv(spyfilepath, sep = ",")
    spylength = len(spy.index)
    spy = spy.round(2)
    spy = AddDataFields.addPercentChanges(spy, spylength)

    for filename in all_files:
        print("current file: ", filename)
        df = pd.read_csv(filename, sep=",", index_col=None, header=0)
        length = len(df.index)
        df = df.round(2)
        df = AddDataFields.addPercentChanges(df, length)
        length = len(df.index) #need to do it a second time because addPercentChanges trims the dataset based on given date
        df = AddDataFields.marketData(df, length, spy)
        df = AddDataFields.addOtherData(df, length)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)

    #make sure output file is not in "path" because then it gets included in "all_files"
    frame.to_csv(outputfile, sep = '\t', index= False)


importdatagroup()
print("DONE GROUP")
