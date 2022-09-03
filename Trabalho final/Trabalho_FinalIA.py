import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
import time


class CasasSp:
    def __init__(self):
        self.data = pd.DataFrame(pd.read_csv("Casas_SP_Final.csv"))
        self.train_x = None
        self.train_y = None
        self.test_x = None
        self.test_y = None

    def exibe_outliers(self):
        data = self.data
        fig, axs = plt.subplots(2, 3, figsize=(10, 5))
        plt1 = sns.boxplot(x=data['CEP'].astype(str).astype(int), ax=axs[0, 0])
        plt2 = sns.boxplot(x=data['AREA'], ax=axs[0, 1])
        plt3 = sns.boxplot(x=data['QUARTOS'], ax=axs[0, 2])
        plt4 = sns.boxplot(x=data['BANHEIROS'], ax=axs[1, 0])
        plt5 = sns.boxplot(x=data['VAGAS'], ax=axs[1, 1])
        plt6 = sns.boxplot(x=data['PRECO'], ax=axs[1, 2])
        plt.tight_layout()
        plt.show()

    def trata_outliers(self, caracteristica):
        Q1 = self.data[caracteristica].quantile(0.25)
        Q3 = self.data[caracteristica].quantile(0.75)
        IQR = Q3 - Q1
        self.data = self.data[
            (self.data[caracteristica] >= Q1 - 1.5 * IQR) & (self.data[caracteristica] <= Q3 + 1.5 * IQR)]

    def correlacoes(self):
        data = self.data
        np.random.seed(0)
        df_train, df_test = train_test_split(data, train_size=0.7, test_size=0.3, random_state=100)
        scaler = MinMaxScaler()
        num_vars = ['CEP', 'AREA', 'QUARTOS', 'BANHEIROS', 'VAGAS', 'PRECO']
        df_train[num_vars] = scaler.fit_transform(df_train[num_vars])
        plt.figure(figsize=(56, 50))
        sns.heatmap(df_train.corr(), annot=True, cmap="YlGnBu")
        plt.show()

    def separa_dados(self):
        data = self.data
        X = data[['CEP', 'AREA', 'QUARTOS', 'BANHEIROS', 'VAGAS']]
        Y = data['PRECO']
        self.train_x, self.test_x, self.train_y, self.test_y = train_test_split(X, Y, test_size=0.3, random_state=1)

    def separa_area(self):
        data = self.data
        X = data['AREA']
        Y = data['PRECO']
        self.train_x, self.test_x, self.train_y, self.test_y = train_test_split(X, Y, test_size=0.3, random_state=10)

    @staticmethod
    def reshape(trainx, testx):
        train_x = np.array(trainx)
        train_x = train_x.reshape(-1, 1)
        test_x = np.array(testx)
        test_x = test_x.reshape(-1, 1)
        return train_x, test_x

    def regressao(self):
        start_time = time.time()
        train_x = self.train_x
        test_x = self.test_x
        train_y = self.train_y
        test_y = self.test_y
        # Caso so haja uma coluna sendo analisada
        if len(np.array(test_x).shape) == 1:
            train_x, test_x = self.reshape(train_x, test_x)
        regression = LinearRegression()
        regression.fit(train_x, train_y)
        print("Score de acuracia Regressao Linear: ")
        print(regression.score(test_x, test_y))
        print(f"Tempo de execucao regressao linear: {(time.time() - start_time)}")
        print("--------------------------------------")
        y_pred = regression.predict(test_x)
        df_preds = pd.DataFrame({'Preco Atual': test_y.squeeze(), 'Preco previsto pela regressao': y_pred.squeeze()})
        df_preds.to_csv('resultado_regressao.csv', index=False)

    def knn(self):
        start_time = time.time()
        train_x = self.train_x
        test_x = self.test_x
        train_y = self.train_y
        test_y = self.test_y
        # Caso so haja uma coluna sendo analisada
        if len(np.array(test_x).shape) == 1:
            train_x, test_x = self.reshape(train_x, test_x)

        # Parte que foi utilizada para se obter o melhor n para o knn, no caso, 4
        # melhor_score = 0
        # melhor_n = 0
        # for i in range(1, 11):
        #    knn = KNeighborsRegressor(n_neighbors=i)
        #    knn.fit(train_x, train_y)
        #    score = knn.score(test_x, test_y)
        #    if score > melhor_score:
        #        melhor_score = score
        #        melhor_n = i
        # print(melhor_n)

        knn = KNeighborsRegressor(n_neighbors=4)
        knn.fit(train_x, train_y)
        print("Score de acuracia KNN regressao: ")
        print(knn.score(test_x, test_y))
        print(f"Tempo de execucao knn: {(time.time() - start_time)}")
        print("--------------------------------------")
        y_pred = knn.predict(test_x)
        df_preds = pd.DataFrame({'Preco Atual': test_y.squeeze(), 'Preco previsto pela regressao': y_pred.squeeze()})
        df_preds.to_csv('resultado_knnr.csv', index=False)


if __name__ == "__main__":
    casas = CasasSp()
    casas.exibe_outliers()
    casas.trata_outliers('PRECO')
    casas.trata_outliers('QUARTOS')
    casas.trata_outliers('AREA')
    casas.trata_outliers('VAGAS')
    casas.exibe_outliers()
    casas.correlacoes()
    casas.separa_dados()
    casas.regressao()
    casas.knn()
    print("Analise apenas com a area:\n")
    casas.separa_area()
    casas.regressao()
    casas.knn()
