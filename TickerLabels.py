import pandas as pd
import glob
import os
import yfinance as yf

#paths to change for local use
folderpath = "/Users/nrosenor/Desktop/CS 578/CS578-Final-Proj/Development Dataset"
outputfile = "/Users/nrosenor/Desktop/CS 578/CS578-Final-Proj/Development Dataset/labels.csv"

def labels():
    # read in files
    path = folderpath
    all_files = glob.glob(os.path.join(path , "*.txt"))
    #exclude combined.txt for dev purposes
    all_files.remove("/Users/nrosenor/Desktop/CS 578/CS578-Final-Proj/Development Dataset/combined.txt")

    tickers = [pd.read_csv(filename)["<TICKER>"][0] for filename in all_files]
    stock_list = [[key, catch(get_sector, key[:-3].split("-")[0]), catch(get_industry, key[:-3].split("-")[0])] for key in tickers]

    df = pd.DataFrame(stock_list, columns = ['<TICKER>', "sector", "industry"])
    df.to_csv(outputfile, index=False)
    
    return

def join_labels_combined():
    labels = pd.read_csv("/Users/nrosenor/Desktop/CS 578/CS578-Final-Proj/Development Dataset/labels.csv")
    combined = pd.read_csv("/Users/nrosenor/Desktop/CS 578/CS578-Final-Proj/Development Dataset/combined.txt", sep = "\t")

    combined = combined.merge(labels, on = '<TICKER>', how = 'left')
    combined.to_csv("/Users/nrosenor/Desktop/CS 578/CS578-Final-Proj/Development Dataset/combined.txt")

    return

# error handling to help labels()
def catch(func, *args, handle=lambda e : e, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return "NA"

# helpers for labels()
def get_sector(ticker):
    return yf.Ticker(ticker).info['sector']

def get_industry(ticker):
    return yf.Ticker(ticker).info['industry']

#labels()

#join_labels_combined()