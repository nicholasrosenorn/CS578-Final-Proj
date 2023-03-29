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
outputfile = r"C:\Users\imhun\Documents\CS 578\Project\Data set\Development Dataset\combined.txt"
singlefilepath = r"C:\Users\imhun\Documents\CS 578\Project\Data set\Development Dataset\aac.us.txt"



#using to test methods on single text files
def importdata():
    df = pd.read_csv(singlefilepath, sep=",")
    print(df)
    length = len(df.index)
    print(df[0:1])
    print(df[length-1:length])
    df = df.round(2)

    AddDataFields.addAll(df, length)
    print(df)
    #df.astype({'<CHANGE>': '.2f'})
    print(df.dtypes)
    
    df.to_csv(r"C:\Users\imhun\Documents\CS 578\Project\Data set\Development Dataset\aac.us_test.txt", sep = '\t')
    




importdata()
print("DONE")


#using to test methods on group of text files
def importdatagroup():
    path = folderpath
    all_files = glob.glob(os.path.join(path , "*.txt"))

    li = []

    print(path)
    print(all_files)
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)

    frame.to_csv(outputfile, sep = '\t')

    


#importdatagroup()