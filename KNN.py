import csv  # Biblioteca que tive que importar para poder ler o csv
from math import sqrt  # Funcao para tirar raiz quadrada
from math import inf  # Definicao do infinito


class KNN:
    def __init__(self, caminho_csv):
        lista = []
        with open(caminho_csv) as csvfile:
            objeto_csv = csv.reader(csvfile)
            for linha in objeto_csv:
                lista.append(linha)
            lista.pop(0)
        self.lista = lista

    @staticmethod
    def dist_euclidiana(x, y):
        somatorio = 0
        for xi, yi in zip(x[1:-1], y[1:-1]):
            somatorio += pow(float(xi) - yi, 2)
        distancia = sqrt(somatorio)
        return distancia

    @staticmethod
    def mais_comum(semelhante):
        return max(set(semelhante), key=semelhante.count)

    def semelhante_vizinhanca(self, y, k):
        k_proximos = []
        for i in range(0,k):
            k_proximos.append([inf, '?']) # Inicializacao da melhor distancia como infinito e a classe como ?
        for x in self.lista:
            distancia = self.dist_euclidiana(x, y)
            for k in k_proximos:
                if distancia < k[0]:
                    k[0] = distancia
                    k[1] = x[-1]
                    break
        especies_proximas = [i[1] for i in k_proximos]
        especie = self.mais_comum(especies_proximas)
        return especie


if __name__ == '__main__':
    # Disponivel em https://www.kaggle.com/datasets/saurabh00007/iriscsv
    knn = KNN('Iris.csv')
    k = int(input('Digite o valor de K: '))
    testes = [
        [2, 4.9, 3.0, 1.4, 0.2, '?'],
        [3, 4.7, 3.2, 1.3, 0.2, '?'],
        [6, 5.4, 3.9, 1.7, 0.4, '?'],
        [10, 4.9, 3.1, 1.5, 0.1, '?'],
        [13, 4.8, 3.0, 1.4, 0.1, '?'],
        [16, 5.7, 4.4, 1.5, 0.4, '?'],
        [18, 5.1, 3.5, 1.4, 0.3, '?'],
        [19, 5.7, 3.8, 1.7, 0.3, '?'],
        [22, 5.1, 3.7, 1.5, 0.4, '?'],
        [26, 5.0, 3.0, 1.6, 0.2, '?'],
        [27, 5.0, 3.4, 1.6, 0.4, '?'],
        [34, 5.5, 4.2, 1.4, 0.2, '?'],
        [38, 4.9, 3.1, 1.5, 0.1, '?'],
        [44, 5.0, 3.5, 1.6, 0.6, '?'],
        [46, 4.8, 3.0, 1.4, 0.3, '?'],
        [49, 5.3, 3.7, 1.5, 0.2, '?'],
        [52, 6.4, 3.2, 4.5, 1.5, '?'],
        [54, 5.5, 2.3, 4.0, 1.3, '?'],
        [57, 6.3, 3.3, 4.7, 1.6, '?'],
        [60, 5.2, 2.7, 3.9, 1.4, '?'],
        [29, 5.2, 3.4, 1.4, 0.2, '?'],
        [33, 5.2, 4.1, 1.5, 0.1, '?'],
        [35, 4.9, 3.1, 1.5, 0.1, '?'],
        [37, 5.5, 3.5, 1.3, 0.2, '?'],
        [43, 4.4, 3.2, 1.3, 0.2, '?'],
        [48, 4.6, 3.2, 1.4, 0.2, '?'],
        [53, 6.9, 3.1, 4.9, 1.5, '?'],
        [55, 6.5, 2.8, 4.6, 1.5, '?'],
        [62, 5.9, 3.0, 4.2, 1.5, '?'],
        [63, 6.0, 2.2, 4.0, 1.0, '?'],
        [67, 5.6, 3.0, 4.5, 1.5, '?'],
        [71, 5.9, 3.2, 4.8, 1.8, '?'],
        [76, 6.6, 3.0, 4.4, 1.4, '?'],
        [81, 5.5, 2.4, 3.8, 1.1, '?'],
        [82, 5.5, 2.4, 3.7, 1.0, '?'],
        [91, 5.5, 2.6, 4.4, 1.2, '?'],
        [93, 5.8, 2.6, 4.0, 1.2, '?'],
        [96, 5.7, 3.0, 4.2, 1.2, '?'],
        [111, 6.5, 3.2, 5.1, 2.0, '?'],
        [121, 6.9, 3.2, 5.7, 2.3, '?'],
        [127, 6.2, 2.8, 4.8, 1.8, '?'],
        [136, 7.7, 3.0, 6.1, 2.3, '?'],
        [141, 6.7, 3.1, 5.6, 2.4, '?'],
        [148, 6.5, 3.0, 5.2, 2.0, '?'],
    ]
    for teste in testes:
        print(knn.semelhante_vizinhanca(teste, k))
