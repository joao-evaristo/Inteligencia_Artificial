#Problemma 1756 do Beecrowd. Disponivel em https://www.beecrowd.com.br/judge/pt/problems/view/1756

def fazer_combinacao(ind1, ind2, corte):
    filho1 = ind1[:corte] + ind2[corte:]
    filho2 = ind2[:corte] + ind1[corte:]
    return [filho1, filho2]

def compara_objetivo(ind, obj):
    match = []
    for i in range(0, len(ind)):
        if ind[i] == obj[i]:
            match.append('s')
        else:
            match.append('n')
    return match

def mutacao(ind, obj, pmut):
    match = compara_objetivo(ind, obj)
    prob_ind = 1
    for i in match:
        if i == 's':
            prob_ind = prob_ind * (1-pmut)
        else:
            prob_ind = prob_ind * (pmut)
    return prob_ind

def probabilidade_geral(p1, p2):
    pgeral = p1 + p2 - (p1*p2)
    pgeral = f'{pgeral:.7f}'
    return (pgeral)

def algoritmo_genetico(input):
    for teste in input:
        ind1 = teste[2]
        ind2 = teste[3]
        obj = teste[4]
        corte = teste[0]
        pmut = teste[1]
        filhos = fazer_combinacao(ind1, ind2, corte)
        p1 = mutacao(filhos[0], obj, pmut)
        p2 = mutacao(filhos[1], obj, pmut)
        print(probabilidade_geral(p1, p2))

if __name__ == "__main__":
    testes = []
    T = int(input())
    for i in range(0,T):
        teste = []
        N = int(input())
        Y, P = input().split()
        Y, P = int(Y), float(P)
        individuo_1 = [int(n) for n in str(input())]
        individuo_2 = [int(n) for n in str(input())]
        possivel_individuo = [int(n) for n in str(input())]
        testes.extend([[Y, P, individuo_1, individuo_2, possivel_individuo]])
    algoritmo_genetico(testes)