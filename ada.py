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

no_iter = 10
best_hyper = list()
top_scores = np.zeros(no_iter)

label_no = len(df_Y.columns)
scores = np.zeros((label_no,no_iter))
for k in range(no_iter):
    #train, validate, test
    trainSet = df_X.sample(frac=.8)
    rest20 = df_X.drop(trainSet.index)
    validateSet = rest20.sample(frac=.5)
    testSet = rest20.drop(validateSet.index)


    train_list = trainSet.index
    train_list = train_list.tolist()

    vali_list = validateSet.index
    vali_list = vali_list.tolist()


    for i in range(label_no):
        X_train = trainSet.to_numpy()
        Y_train = df_Y[df_Y.index.isin(train_list)].to_numpy()[:,i]

        clf = AdaBoostClassifier(n_estimators=100,random_state=0).fit(X_train, Y_train)
        X_vali = validateSet.to_numpy()
        Y_vali = df_Y[df_Y.index.isin(vali_list)].to_numpy()[:, i]

        scores[i,k] = clf.score(X_vali, Y_vali)
        #print('Test' + str(i) + '...DONE:' + str(scores[i]))


    hyper_para = np.argmax(scores[:,k])
    hyper = df_Y.columns[hyper_para]


    X_test = rest20.drop(validateSet.index).to_numpy()

    test_list = testSet.index
    test_list = test_list.tolist()

    Y_test = df_Y[df_Y.index.isin(test_list)].to_numpy()[:, hyper_para]
    top_score = clf.score(X_test, Y_test)
    print('Iter: '+str(k) + ' Hyper: ' + hyper + ' Score: ' + str(top_score))
    best_hyper.append(hyper)
    top_scores[k]=top_score


plt.hist(top_scores, 50, density=True)
plt.show()
print(scores)

avgs = np.zeros(label_no)
st = np.zeros(label_no)
for i in range(label_no):
    avgs[i] = np.average(scores[i,:])
    st[i] = np.std(scores[i,:])

print(avgs)
print(st)








