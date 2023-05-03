from sklearn.ensemble import AdaBoostClassifier
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections


'''<TICKER>,<DATE>,<CLOSE>,<CHANGE>,<22Day>,<44Day>,<66Day>,<HV>,<SPY_CHANGE>,<SPY_HV>,
<BETA>,<F_22Day>,<F_44Day>,<F_66Day>,1 Yr,Price22_1,Profit22_1,lable22_1,Price22_0.95,
Profit22_0.95,lable22_0.95,Price22_0.9,Profit22_0.9,lable22_0.9,Price22_0.85,Profit22_0.85,
lable22_0.85,Price44_1,Profit44_1,lable44_1,Price44_0.95,Profit44_0.95,lable44_0.95,
Price44_0.9,Profit44_0.9,lable44_0.9,Price44_0.85,Profit44_0.85,lable44_0.85,Price66_1,
Profit66_1,lable66_1,Price66_0.95,Profit66_0.95,lable66_0.95,Price66_0.9,Profit66_0.9,
lable66_0.9,Price66_0.85,Profit66_0.85,lable66_0.85,<SECTOR>,<INDUSTRY>'''

def load_data():
    mldata = r"C:\Users\johnp\Documents\S2023\CS578\CS578-Final-Proj-main\Development Dataset\MLdata_hyper.txt"
    df = pd.read_csv(mldata, sep=",")
    #df_new = df.drop(['<TICKER>', '<DATE>'], axis=1)
    df['<PHARM>'] = (df['<SECTOR>'] == 'Healthcare').astype(int)
    # print(df_new)
    df = df.dropna()
    df['DATE'] = pd.to_datetime(df['<DATE>'])
    df = df.sort_values(by='DATE',ignore_index=True)
    df = df.drop(['<DATE>'],axis=1)
    print(df)
    # print(df_new)
    df_X = df
    df_Y = df
    df_X = df_X.drop(['lable22_1','lable22_0.95','lable22_0.9','lable22_0.85','lable44_1','lable44_0.95',
               'lable44_0.9','lable44_0.85','lable66_1','lable66_0.95','lable66_0.9','lable66_0.85',
                      '<SECTOR>', '<INDUSTRY>', '<BETA>', '<F_22Day>',
                      '<F_44Day>', '<F_66Day>', '1 Yr','Profit22_1',
                      'Profit22_0.95','Profit22_0.9',
                      'Profit44_1','Profit44_0.95',
                      'Profit44_0.9','Profit44_0.85',
                      'Profit66_1','Profit66_0.95','Profit66_0.9',
                      'Profit66_0.85','<SECTOR>','<INDUSTRY>','<BETA>','<F_22Day>',
                     '<F_44Day>','<F_66Day>'],axis=1)
    df_Y = df_Y.drop(['<CLOSE>','<CHANGE>','<22Day>','<44Day>','<66Day>',
                     '<HV>','<SPY_CHANGE>','<SPY_HV>','Price22_1','Profit22_1','Price22_0.95',
                      'Profit22_0.95','Price22_0.9','Profit22_0.9','Price22_0.85',
                      'Profit22_0.85','Price44_1','Profit44_1','Price44_0.95','Profit44_0.95',
                      'Price44_0.9','Profit44_0.9','Price44_0.85','Profit44_0.85','Price66_1',
                      'Profit66_1','Price66_0.95','Profit66_0.95','Price66_0.9','Profit66_0.9',
                      'Price66_0.85','Profit66_0.85','<SECTOR>','<INDUSTRY>','<BETA>','<F_22Day>',
                     '<F_44Day>','<F_66Day>','1 Yr','<PHARM>'],axis=1)
    return df_X, df_Y

df_X, df_Y = load_data()

stock_info = df_X[['<TICKER>','DATE']]



profit = df_X['Profit22_0.85']
df_X = df_X.drop(['Profit22_0.85'],axis=1)

df_X = df_X.drop(['DATE', '<TICKER>'],axis=1)

label = df_Y['lable22_0.85']


#create model

trainSet = df_X.iloc[:int(0.8*40300)]
rest20 = df_X.drop(trainSet.index)

train_list = trainSet.index
train_list = train_list.tolist()

rest_list = rest20.index
rest_list = rest_list.tolist()


X_train = trainSet.to_numpy()
Y_train = label[label.index.isin(train_list)].to_numpy()




clf = AdaBoostClassifier(n_estimators=100,random_state=0).fit(X_train, Y_train)

stock_info = stock_info[stock_info.index.isin(rest_list)]
stock_name = stock_info['<TICKER>'].tolist()
stock_date = stock_info['DATE'].tolist()


# test on new data
Y_test = label[label.index.isin(rest_list)].to_numpy()
profit = profit[profit.index.isin(rest_list)].to_numpy()
c = 0
money = np.zeros(len(profit))
money[0] = 5000
miss_rate = 0
total_predictions = 0
#print(stock_info)
misses = list()
hits = list()
missed_hits = list()
correct_miss = list()
for i, row in rest20.iterrows():
    if (c == 0):
        print(stock_date[c])
    #print(row)
    n = clf.predict(row.to_numpy().reshape(1,-1))

    #print(row.to_numpy().reshape(1,-1))
    if (n==0 and Y_test[c] == 0):
        correct_miss.append(row['Price22_0.85'])
    if (n == 0 and Y_test[c] == 1):
        missed_hits.append(profit[c] - row['Price22_0.85'])
    if (n == 1 and c > 0):
        total_predictions += 1
        money[c] = money[c-1] - row['Price22_0.85']

        if (n == Y_test[c]):
            #print('Profit: ' + str(profit[c]))
            money[c] += profit[c]
            hits.append(profit[c] - row['Price22_0.85'])
            if (profit[c] >= 100):
                print('Stock: ' + stock_name[c])
                print('Date: ' + str(stock_date[c]))
                print('Profit: ' + str(profit[c]))
        else:
            miss_rate += 1
            misses.append(row['Price22_0.85'])
            #print('DUMBASS: ' + str(row['Price22_0.85']))
    if (n == 0):
        if (c > 0):
            money[c] = money[c-1]


    c += 1



print(miss_rate/total_predictions)
print(money[c - 1] / money[0])
plt.plot(stock_info['DATE'],money)
plt.show()

stock_info['money'] = money
stock_info['spy'] = rest20['<SPY_CHANGE>']

#stock_info.to_csv('stuff.csv')
print(sum(misses) / len(misses))
print(len(misses))
print(sum(hits) / len(hits))
print(len(hits))
print(sum(missed_hits) / len(missed_hits))
print(len(missed_hits))
print(sum(correct_miss) / len(correct_miss))
print(len(correct_miss))

print(clf.score(rest20,Y_test))


