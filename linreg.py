from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd

mldata = r"C:\Users\johnp\Documents\S2023\CS578\CS578-Final-Proj-main\Development Dataset\MLdata.txt"

df = pd.read_csv(mldata, sep="\t")
print(df)
df_new=df.drop(['<TICKER>','<DATE>'], axis=1)

#print(df_new)
df_new = df_new.dropna()
#print(df_new)

df_new = df_new.drop(['<PROFIT>'],axis=1)

#separate data
print(df_new)
trainSet = df_new.sample(frac=.7)
print(trainSet)
rest20 = df_new.drop(trainSet.index)
validateSet = rest20.sample(frac=.4)
testSet = rest20.drop(validateSet.index)

Y_train = trainSet['<LABEL>'].to_numpy()
trainSet = trainSet.drop('<LABEL>',axis=1)

Y_test = testSet['<LABEL>'].to_numpy()
testSet = testSet.drop('<LABEL>',axis=1)

X_train = trainSet.to_numpy()
print(X_train)

X_test = testSet.to_numpy()

clf = LogisticRegression(random_state=0,max_iter=int(1e14)).fit(X_train,Y_train)
print(clf.score(X_test,Y_test))

#print(clf.predict_proba(X_test))
#print(clf.decision_function(X_test))
