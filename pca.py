

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd




def load_data():
    mldata = r"C:\Users\johnp\Documents\S2023\CS578\CS578-Final-Proj-main\Development Dataset\MLdata1.txt"

    df = pd.read_csv(mldata, sep=",")
    print(df)
    df_new = df.drop(['<TICKER>', '<DATE>'], axis=1)
    print('hi')
    df_new['<PHARM>'] = (df_new['<SECTOR>'] == 'Healthcare').astype(int)
    df_new = df_new.drop(['<SECTOR>', '<INDUSTRY>'], axis=1)
    # print(df_new)
    df_new = df_new.dropna()
    # print(df_new)

    df_new = df_new.drop(['<PROFIT>', '<F_22Day>', '<F_44Day>', '<F_66Day>', ], axis=1)
    return df_new

df = load_data()



y = df['<LABEL>'].to_numpy()
X = df.drop(['<LABEL>'],axis=1).to_numpy()
print(X)
pca = PCA(n_components=3)
pca.fit(X)
Xt = pca.transform(X)
print(Xt)
fig = plt.figure()
ax = fig.add_subplot(projection='3d')


plot = ax.scatter(Xt[:,0], Xt[:,1], Xt[:,2], c=y)
plot = plt.sca
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')

#plt.legend(handles=plot.legend_elements()[0], labels={1,0})
plt.show()

