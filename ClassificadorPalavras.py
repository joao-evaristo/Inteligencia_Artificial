import numpy as np
from re import sub
import requests
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans as kmeans
from pandas import DataFrame


class ClassificadorPalavras:
    def __init__(self):
        self.bag_words = np.array(0)
        self.bag_aux = np.array(0)
        # Disponivel em https://www.kaggle.com/datasets/crawford/20-newsgroups?resource=download&select=talk.politics.guns.txt
        with open('talk.politics.guns.txt', 'r') as file:
            texto1 = sub(r"[^a-zA-Z0-9]+", ' ', file.read())
            texto1 = texto1.lower()
            self.texto1 = texto1
            file.close()
        # Disponivel em https://www.kaggle.com/datasets/crawford/20-newsgroups?resource=download&select=talk.religion.misc.txt
        with open('talk.religion.misc.txt', 'r') as file:
            texto2 = sub(r"[^a-zA-Z0-9]+", ' ', file.read())
            texto2 = texto2.lower()
            self.texto2 = texto2
            file.close()
        self.train_x = np.array(0)
        self.train_y = np.array(0)
        self.test_x = np.array(0)
        self.test_y = np.array(0)

    def bag_of_words(self):
        texto1 = self.texto1
        texto2 = self.texto2
        dict_aux = {}
        join_texto = texto1 + ' ' + texto2
        for palavra in join_texto.split():
            if palavra not in dict_aux.keys():
                dict_aux[palavra] = [1, 1]

        for palavra in texto1.split():
            dict_aux[palavra][0] += 1

        for palavra in texto2.split():
            dict_aux[palavra][1] += 1
        dict_aux['Rótulo'] = [1, 2]
        self.remove_stpwords(dict_aux)
        chaves = list(dict_aux.keys())
        palavras1 = [i[0] for i in dict_aux.values()]
        palavras2 = [i[1] for i in dict_aux.values()]
        self.bag_words = np.matrix([chaves, palavras1, palavras2])
        print(DataFrame(self.bag_words))
        self.bag_aux = np.array([palavras1, palavras2])

    def separa_dados(self):
        self.train_x, self.test_x, self.train_y, self.test_y = train_test_split(self.bag_aux, ['Texto 1', 'Texto 2'], test_size=0.3)

    def knn(self):
        knn = KNeighborsClassifier(n_neighbors = 1)
        y_pred = knn.fit(self.train_x, self.train_y)
        predict = y_pred.predict(self.test_x)
        print(f'Texto pertencente: {predict}')

    def kmeans(self):
        k_means = kmeans(n_clusters=2, init='random')
        k_means.fit(self.bag_aux)
        Y = kmeans.predict(self=k_means, X=self.bag_aux)
        plt.scatter(self.bag_aux[:, 1], self.bag_aux[:, 0], c=Y, s=50, cmap='viridis')
        centers = k_means.cluster_centers_
        plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.5)
        plt.show()

    @staticmethod
    def remove_stpwords(dict):
        stopwords_list = requests.get(
            "https://raw.githubusercontent.com/stopwords-iso/stopwords-en/master/stopwords-en.txt").content
        stopwords = set(stopwords_list.decode().splitlines())
        chaves = list(dict.keys())
        for stpword in stopwords:
            if stpword in chaves:
                dict.pop(stpword)


if __name__ == '__main__':
    classificador = ClassificadorPalavras()
    classificador.bag_of_words()
    classificador.separa_dados()
    classificador.kmeans()
