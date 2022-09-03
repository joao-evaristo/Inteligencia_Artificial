from scipy.cluster.hierarchy import dendrogram, single
from matplotlib import pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
from pandas import read_csv
from sklearn.cluster import AgglomerativeClustering


class SingleLinkage:
    def __init__(self, csv):
        dados = read_csv(csv, usecols=[0, 1])
        self.dados = np.array(dados)

    def clusterizacao(self):
        sin_linkage = single(self.dados)
        fig = plt.figure()
        dn = dendrogram(sin_linkage)
        plt.show()


if __name__ == '__main__':
    Tk().withdraw()
    csv = askopenfilename()
    sl = SingleLinkage(csv)
    sl.clusterizacao()