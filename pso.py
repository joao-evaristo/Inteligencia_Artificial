class PSO:
    def __init__(self, w, c1, c2, r1, r2, n, iteracoes, X, V, funcao):
        self.local_bet = []
        self.global_b_fitness = None
        self.global_b_position = None
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.r1 = r1
        self.r2 = r2
        self.n = n
        self.iteracoes = iteracoes
        self.X = X
        self.V = V

    def inicializar(self):
        self.X = [round((i - 0.5) * 10, 4) for i in self.X]
        self.V = [round((i - 0.5), 4) for i in self.V]
        self.local_bet = self.X

    def velocidade(self, indice):
        w = self.w
        v = self.V[indice]
        c1 = self.c1
        c2 = self.c2
        r1 = self.r1
        r2 = self.r2
        pbest = self.local_bet[indice]
        x = self.X[indice]
        gbest = self.global_b_position
        velocidade = w * v + c1 * r1 * (pbest - x) + c2 * r2 * (gbest - x)
        return round(velocidade, 4)

    def atualiza_pbest(self, fx):
        for i in range(0, self.n):
            if self.funcao(self.X[i]) > fx[i]:
                self.local_bet[i] = self.X[i]

    def funcao(self, x):
        x = x
        return eval(funcao)

    def fitness(self):
        for j in range(0, self.iteracoes):
            print('===================================================================')
            print(f'Local best position = {self.local_bet}')
            fx = [self.funcao(x) for x in self.X]
            self.global_b_fitness = max(fx)
            self.global_b_position = self.X[fx.index(self.global_b_fitness)]
            print(f'Global best fitness = {self.global_b_fitness}')
            print(f'Global best position = {self.global_b_position}')
            # Atualiza os valores para próxima iteração
            self.V = [self.velocidade(i) for i in range(0, self.n)]
            self.X = [round((self.X[i] + self.V[i]), 3) for i in range(0, self.n)]
            self.atualiza_pbest(fx)


if __name__ == '__main__':
    w = float(input('w: '))
    c1 = float(input('c1: '))
    c2 = float(input('c2: '))
    r1 = float(input('r1: '))
    r2 = float(input('r2: '))
    n = int(input('n: '))
    iteracoes = int(input('Iterações: '))
    X = [float(x) for x in input('Vetor de X separado por virgulas: ').split(',')]
    V = [float(x) for x in input('Vetor de V separado por virgulas: ').split(',')]
    funcao = input('Função: ')
    pso = PSO(w, c1, c2, r1, r2, n, iteracoes, X, V, funcao)
    pso.inicializar()
    pso.fitness()
