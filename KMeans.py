from matplotlib import pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
from pandas import read_csv
from sklearn.cluster import KMeans as kmeans


class KMeans:
    def __init__(self, csv):
        dados = read_csv(csv, usecols=[0, 1])
        self.dados = np.array(dados)

    def clusterizacao(self, k):
        X = self.dados
        k_means = kmeans(n_clusters=k, init='random')
        k_means.fit(X)
        Y = kmeans.predict(self=k_means, X=X)
        plt.scatter(X[:, 1], X[:, 0], c=Y, s=50, cmap='viridis')
        centers = k_means.cluster_centers_
        plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.5)
        plt.show()


if __name__ == '__main__':
    Tk().withdraw()
    csv = askopenfilename()
    km = KMeans(csv)
    k = int(input('Digite o valor de k: '))
    km.clusterizacao(k)
