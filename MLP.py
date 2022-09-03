from tkinter import Tk
from tkinter.filedialog import askopenfilename
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


class MLP:
    def __init__(self, csv_file):
        self.model = None
        classes = []
        self.dados = np.array(pd.read_csv(csv_file))
        for i, linha in enumerate(self.dados):
            if i == 0:
                continue
            if linha[5] not in classes:
                classes.append(linha[5])
        self.classes = classes
        self.train_x = np.array(0)
        self.train_y = np.array(0)
        self.test_x = np.array(0)
        self.test_y = np.array(0)
        self.topology = []
        self.num_x = []
        self.num_y = []

    def separa_dados(self):
        dados = self.dados
        scaler = StandardScaler()
        y = np.array(pd.get_dummies(dados[:, dados.shape[1] - 1])).astype(np.float32)
        x = (dados[:, :(dados.shape[1] - 1)]).astype(np.float32)
        scaler.fit(x)  # ajuste do scaler para pré-processamento
        # Gerando os conjuntos de treinamento e teste (validação)
        self.train_x, self.test_x, self.train_y, self.test_y = train_test_split(x, y,
                                                                                test_size=0.30)  # 0.30 dos dados no conjunto de teste
        print('Conjuntos de treinamento e teste separados!')

    def topologia(self):
        print('Ajustando a topologia...')
        self.num_x = self.train_x.shape[1]
        self.num_y = self.train_y.shape[1]
        print('Entradas = %i\nSaídas = %i' % (self.num_x, self.num_y))

        while True:
            num_hidden_layers = int(input('Número de camadas ocultas: '))
            if num_hidden_layers > 0:
                break

        if num_hidden_layers == 1:
            while True:
                self.topology = [int(input('Neurônios na camada oculta: '))]
                if self.topology[0] > 0:
                    break
        else:
            for i in range(num_hidden_layers):
                while (True):
                    num = int(input('Neurônios na %iª camada oculta: ' % (i + 1)))
                    if num > 0:
                        self.topology.append(num)
                        break

    def treinamento(self):
        topology = self.topology
        num_x = self.num_x
        num_y = self.num_y
        scaler = StandardScaler()
        print('\n\nTreinamento...')

        epochs = int(input('Número de épocas de treinamento: '))

        # inicialização do modelo
        Model = MLPClassifier(hidden_layer_sizes=tuple(topology), max_iter=epochs, alpha=0.1,
                              solver='sgd', learning_rate_init=0.01, momentum=0.9, learning_rate='adaptive', verbose=0,
                              random_state=121)

        topology.insert(0, num_x)
        topology.append(num_y)

        # pré-processamento
        scaler.fit(self.train_x)
        p_train_x = scaler.transform(self.train_x)

        # treinando o modelo
        self.model = Model.fit(p_train_x, self.train_y)

        print(self.model)
        print('Topologia da MLP =', topology)

    def acuracia(self):
        # pré-processamento
        scaler = StandardScaler()
        test_x = self.test_x
        test_y = self.test_y
        scaler.fit(test_x)
        p_test_x = scaler.transform(test_x)

        test_est_y = self.model.predict(p_test_x)

        # matriz de confusão
        mat = confusion_matrix(test_y.argmax(axis=1), test_est_y.argmax(axis=1))
        sns.heatmap(mat.T, square=True, annot=True, fmt='d', cbar=False, xticklabels=self.classes,
                    yticklabels=self.classes)
        plt.xlabel('Real')
        plt.ylabel('Estimado')
        plt.show()
        print('A acurácia é ', accuracy_score(test_est_y, test_y))  # exibe acurácia


if __name__ == '__main__':
    Tk().withdraw()
    csv = askopenfilename()
    mlp = MLP(csv)
    mlp.separa_dados()
    mlp.topologia()
    mlp.treinamento()
    mlp.acuracia()
