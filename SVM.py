from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import svm


class SVM:
    def __init__(self, csv_file):
        classes = []
        y = np.array(0)
        self.dados = np.array(pd.read_csv(csv_file))
        for i, linha in enumerate(self.dados):
            if i == 0:
                continue
            if linha[5] not in classes:
                classes.append(linha[5])
            y = np.append(y, len(classes) - 1)
        self.x = np.array(self.dados[:, 1:-1])
        self.y = y
        self.train_x = np.array(0)
        self.train_y = np.array(0)
        self.test_x = np.array(0)
        self.test_y = np.array(0)

    def separa_dados(self):

        self.train_x, self.test_x, self.train_y, self.test_y = train_test_split(self.x, self.y, test_size=0.30)  # 0.30 dos dados no conjunto de teste
        print('Conjuntos de treinamento e teste separados!')

    def classificacao(self):
        cfl = svm.SVC(kernel='linear', C=1.0)
        cfl.fit(self.train_x, self.train_y)
        score = cfl.score(self.test_x, self.test_y)
        print(f'A acurácia é {score}')


if __name__ == '__main__':
    Tk().withdraw()
    csv = askopenfilename()
    mlp = SVM(csv)
    mlp.separa_dados()
    mlp.classificacao()
