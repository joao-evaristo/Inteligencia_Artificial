import csv  # Biblioteca que tive que importar para poder ler o csv


class NaiveBayes:
    def __init__(self, caminho_csv):
        lista = []
        with open(caminho_csv) as csvfile:
            objeto_csv = csv.reader(csvfile)
            for linha in objeto_csv:
                lista.append(linha)
            aux = lista.pop(0)
        self.lista = lista
        self.dict_tabela = {}
        for info in aux[1:]:
            self.dict_tabela[info] = []
        self.lista_discretizada = []

    def discretiza_lista(self):
        for individuo in self.lista:
            indivo_disc = self.discretizar(individuo)
            self.lista_discretizada.append(indivo_disc)

    @staticmethod
    def discretizar(individuo):
        lista_aux = [individuo[0]]

        # comprimento sepala
        sepal_lenght = float(individuo[1])
        if sepal_lenght < 5.4:
            sepal_lenght = 'pequeno'
        elif 5.4 <= sepal_lenght <= 6.2:
            sepal_lenght = 'medio'
        else:
            sepal_lenght = 'grande'
        lista_aux.append(sepal_lenght)

        # largura da sepala
        sepal_width = float(individuo[2])
        if sepal_width < 2.9:
            sepal_width = 'pequeno'
        elif 2.9 <= sepal_width <= 3.3:
            sepal_width = 'medio'
        else:
            sepal_width = 'grande'
        lista_aux.append(sepal_width)

        # comprimento da petala
        petal_lenght = float(individuo[3])
        if petal_lenght < 3.4:
            petal_lenght = 'pequeno'
        elif 3.4 <= petal_lenght <= 5.0:
            petal_lenght = 'medio'
        else:
            petal_lenght = 'grande'
        lista_aux.append(petal_lenght)

        # largura da petala
        petal_width = float(individuo[3])
        if petal_width < 0.7:
            petal_width = 'pequeno'
        elif 0.7 <= petal_width <= 1.6:
            petal_width = 'medio'
        else:
            petal_width = 'grande'
        lista_aux.append(petal_width)

        # classe
        lista_aux.append(individuo[5])

        return lista_aux

    def organiza_dados(self):
        for caracteristica in self.dict_tabela:
            index_caracteristica = list(self.dict_tabela.keys()).index(caracteristica) + 1
            # Estimador de Laplace
            pequeno_setosa = 1
            pequeno_versicolor = 1
            pequeno_virginica = 1
            medio_setosa = 1
            medio_versicolor = 1
            medio_virginica = 1
            grande_setosa = 1
            grande_versicolor = 1
            grande_virginica = 1

            for individuo in self.lista_discretizada:
                eh_pequeno = individuo[index_caracteristica] == 'pequeno'
                eh_medio = individuo[index_caracteristica] == 'medio'
                eh_grande = individuo[index_caracteristica] == 'grande'
                classe = individuo[5]
                if classe == 'Iris-setosa':
                    if eh_pequeno:
                        pequeno_setosa += 1
                    elif eh_medio:
                        medio_setosa += 1
                    elif eh_grande:
                        grande_setosa += 1

                elif classe == 'Iris-versicolor':
                    if eh_pequeno:
                        pequeno_versicolor += 1
                    elif eh_medio:
                        medio_versicolor += 1
                    elif eh_grande:
                        grande_versicolor += 1

                elif classe == 'Iris-virginica':
                    if eh_pequeno:
                        pequeno_virginica += 1
                    elif eh_medio:
                        medio_virginica += 1
                    elif eh_grande:
                        grande_virginica += 1

            total_setosa = pequeno_setosa + medio_setosa + grande_setosa
            total_versicolor = pequeno_versicolor + medio_versicolor + grande_versicolor
            total_virginica = pequeno_virginica + medio_virginica + grande_virginica
            self.dict_tabela[caracteristica].append(
                ['pequeno', (pequeno_setosa / total_setosa), (pequeno_versicolor / total_versicolor),
                 (pequeno_virginica / total_virginica)])
            self.dict_tabela[caracteristica].append(
                ['medio', (medio_setosa / total_setosa), (medio_versicolor / total_versicolor),
                 (medio_virginica / total_virginica)])
            self.dict_tabela[caracteristica].append(
                ['grande', (grande_setosa / total_setosa), (grande_versicolor / total_versicolor),
                 (grande_virginica / total_virginica)])
            # Para o caso da especie
            if index_caracteristica + 1 == 5:
                total_especies = total_setosa + total_versicolor + total_virginica
                self.dict_tabela['Species'].extend([total_setosa / total_especies, total_versicolor / total_especies,
                                                    total_virginica / total_especies])
                # dict_tabela = {'SepalLengthCm': [['pequeno', probabilidade de ser pequeno e ser Iris Setosa, probabilidade de ser pequeno e ser Iris Versicolor, etc], ....]}
                return

    def calcula_probabilidade(self, especie, individuo):
        atri_comparacoes = list(self.dict_tabela.values())
        probabilidade = 1

        aux_comparacao = []
        for index, atributo_individuo in enumerate(individuo[1:-1]):
            atributo = atri_comparacoes[index]
            if atributo_individuo == 'pequeno':
                aux_comparacao = atributo[0]
            elif atributo_individuo == 'medio':
                aux_comparacao = atributo[1]
            elif atributo_individuo == 'grande':
                aux_comparacao = atributo[2]
            if especie == 'Iris-setosa':
                probabilidade *= float(aux_comparacao[1])
            elif especie == 'Iris-versicolor':
                probabilidade *= float(aux_comparacao[2])
            elif especie == 'Iris-virginica':
                probabilidade *= float(aux_comparacao[3])
        if especie == 'Iris-setosa':
            probabilidade *= float(atri_comparacoes[-1][0])
        elif especie == 'Iris-versicolor':
            probabilidade *= float(atri_comparacoes[-1][1])
        elif especie == 'Iris-virginica':
            probabilidade *= float(atri_comparacoes[-1][2])
        return probabilidade

    def normalizar(self, individuo):
        individuo_disc = self.discretizar(individuo)
        p_setosa = self.calcula_probabilidade('Iris-setosa', individuo_disc)
        p_versicolor = self.calcula_probabilidade('Iris-versicolor', individuo_disc)
        p_virginica = self.calcula_probabilidade('Iris-virginica', individuo_disc)
        if p_setosa > p_versicolor and p_setosa > p_virginica:
            print('Iris-setosa')
        elif p_versicolor > p_setosa and p_versicolor > p_virginica:
            print('Iris-versicolor')
        elif p_virginica > p_setosa and p_virginica > p_versicolor:
            print('Iris-virginica')


if __name__ == '__main__':
    # Disponivel em https://www.kaggle.com/datasets/saurabh00007/iriscsv
    bayes = NaiveBayes('Iris.csv')
    bayes.discretiza_lista()
    bayes.organiza_dados()
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
        bayes.normalizar(teste)