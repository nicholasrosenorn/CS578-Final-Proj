from sklearn.ensemble import AdaBoostClassifier
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections
from sklearn.tree import DecisionTreeClassifier
from sklearn.inspection import DecisionBoundaryDisplay


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
    df_new = df.drop(['<TICKER>', '<DATE>'], axis=1)
    df_new['<PHARM>'] = (df_new['<SECTOR>'] == 'Healthcare').astype(int)
    # print(df_new)
    df_new = df_new.dropna()
    # print(df_new)
    df_X = df_new
    df_Y = df_new
    df_X = df_X.drop(['lable22_1','lable22_0.95','lable22_0.9','lable22_0.85','lable44_1','lable44_0.95',
               'lable44_0.9','lable44_0.85','lable66_1','lable66_0.95','lable66_0.9','lable66_0.85',
                      '<SECTOR>', '<INDUSTRY>', '<BETA>', '<F_22Day>',
                      '<F_44Day>', '<F_66Day>', '1 Yr','Profit22_1',
                      'Profit22_0.95','Profit22_0.9',
                      'Profit22_0.85','Profit44_1','Profit44_0.95',
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

no_iter = 1
best_hyper = list()
top_scores = np.zeros(no_iter)

#train, validate, test
trainSet = df_X.sample(frac=1)
rest20 = df_X.drop(trainSet.index)
validateSet = rest20.sample(frac=.5)
testSet = rest20.drop(validateSet.index)


label_no = len(df_Y.columns)
scores = np.zeros(label_no)



train_list = trainSet.index
train_list = train_list.tolist()

vali_list = validateSet.index
vali_list = vali_list.tolist()



X_train = trainSet.to_numpy()
Y_train = df_Y[df_Y.index.isin(train_list)].to_numpy()[:,3]
fig, ax = plt.subplots(7, 7)
fig.set_size_inches(15,15)

headers = df_X.columns

for i in range(7):
    for j in range(7):
        if (i != j):
            X = X_train[:,[i,j]]



            clf = DecisionTreeClassifier().fit(X, Y_train)


            DecisionBoundaryDisplay.from_estimator(
                clf,
                X,
                cmap=plt.cm.RdYlBu,
                response_method="predict",
                ax=ax[j,i]
            )
        if (j == 7 - 1):
            ax[j,i].set_xlabel(headers[j])
        if (i == 0):
            ax[j,i].set_ylabel(headers[i])

plt.show()











