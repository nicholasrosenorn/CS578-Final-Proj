import pandas as pd
import glob
import os
import yfinance as yf
import Header

#paths to change for local use
folderpath = Header.raw_stock_folder
outputfile = Header.lables_file

def labels():
    # read in files
    path = folderpath
    all_files = glob.glob(os.path.join(path , "*.txt"))
    #exclude combined.txt for dev purposes
    #all_files.remove("/Users/nrosenor/Desktop/CS 578/CS578-Final-Proj/Development Dataset/combined.txt")

    tickers = [pd.read_csv(filename)["<TICKER>"][0] for filename in all_files]
    stock_list = [[key, catch(get_sector, key[:-3].split("-")[0]), catch(get_industry, key[:-3].split("-")[0])] for key in tickers]

    df = pd.DataFrame(stock_list, columns = ['<TICKER>', "sector", "industry"])
    df.to_csv(outputfile, index=False)
    
    return

def join_labels_combined(combined):
    #this is incase combined already has sector and industry attached to it
    if len(combined.columns)  >= 19 :
        return combined

    labels = pd.read_csv(outputfile)
    #combined = pd.read_csv(Header.combined_stock_data, sep = "\t")

    combined = combined.merge(labels, on = '<TICKER>', how = 'left')
    #combined.to_csv(Header.combined_stock_data, sep = '\t', index= False)

    return combined

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