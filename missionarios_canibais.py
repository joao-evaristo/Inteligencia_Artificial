from copy import deepcopy
def pode_mover(matriz, origem, movimento):
    try:
        destino = [origem[0] + movimento[0], origem[1] + movimento[1]]
        testar = matriz[destino[0], destino[1]]
        return destino
    except:
        return -1
#def mover_barco():


def estados_possiveis(estado_atual):#estados possiveis, nao necessariamente resultaram em vitoria ou derrota
    jogadas = []
    if estado_atual["Barco"] == 1:
        ha_canibal = -1 in estado_atual["A"]
        ha_missionario = 2 in estado_atual["A"]
        if ha_canibal:
            aux = deepcopy(estado_atual)
            aux["A"].remove(-1)
            aux["B"].append(-1)
            jogadas.append(aux)
        if ha_missionario:
            aux = deepcopy(estado_atual)
            aux["A"].remove(2)
            aux["B"].append(2)
            jogadas.append(aux)
        if ha_canibal and ha_missionario:
            aux = deepcopy(estado_atual)
            aux["A"].remove(-1)
            aux["B"].append(-1)
            aux["A"].remove(2)
            aux["B"].append(2)
            jogadas.append(aux)
    else:
        ha_canibal = -1 in estado_atual["B"]
        ha_missionario = 2 in estado_atual["B"]
        if ha_canibal:
            aux = deepcopy(estado_atual)
            aux["B"].remove(-1)
            aux["A"].append(-1)
            jogadas.append(aux)
        if ha_missionario:
            aux = deepcopy(estado_atual)
            aux["B"].remove(2)
            aux["A"].append(2)
            jogadas.append(aux)
        if ha_canibal and ha_missionario:
            aux = deepcopy(estado_atual)
            aux["B"].remove(-1)
            aux["A"].append(-1)
            aux["B"].remove(2)
            aux["A"].append(2)
            jogadas.append(aux)
    return jogadas

def perdeu(estado):
    if len(estado["A"]) != 1 and

def jogar(estado):
    #implementando a busca em largura
    caminho_estados = []
    caminho_estados.append(estado)
    fila = [estado]
    estado_final = {"A": [], "B": [-1,-1,-1,2,2,2], "Barco": 0}
    while fila:
        estado_atual = fila.pop(0)
        for escolha in estados_possiveis(estado_atual):
            if escolha == estado_final:
                caminho_estados.append(escolha)
                return caminho_estados
            if !perdeu(escolha)

    return  caminho_estados
def busca_em_largura(matriz, inicio):
    visitados = []
    visitados.append(inicio)
    movimentos_direita_baixo = [[0, 1], [1, 0]]
    fila = [inicio]
    tamanho = len(matriz)
    destino = []
    contador = 0
    destino.extend([tamanho - 1, tamanho -1])
    while fila:
        vertice = fila.pop(0)
        for movimento in movimentos_direita_baixo:
            aux_vertice = pode_mover(matriz, vertice, movimento)
            if aux_vertice == destino:
                contador+=1
            if aux_vertice != -1:
                if matriz[aux_vertice[0], aux_vertice[1]] != '#':
                    visitados.append(aux_vertice)
                    fila.append(aux_vertice)
                else:
                    continue
    if contador == 0:
        visitados = []
        visitados.append(inicio)
        fila = [inicio]
        movimentos_totais = [[0, 1], [1, 0], [-1,0], [0, -1]]
        while fila:
            vertice = fila.pop(0)
            for movimento in movimentos_totais:
                aux_vertice = pode_mover(matriz, vertice, movimento)
                if aux_vertice == destino:
                    contador += 1
                if aux_vertice != -1:
                    if matriz[aux_vertice[0], aux_vertice[1]] != '#' and aux_vertice not in visitados:
                        visitados.append(aux_vertice)
                        fila.append(aux_vertice)
                    else:
                        continue
        if contador != 0:
            return "THE GAME IS A LIE"
        else:
            return "INCONCEIVABLE"

    return contador
if __name__ == "__main__":

    estado_inicial = {"A": [-1,-1,-1,2,2,2], "B": [], "Barco": 1}
    jogar(estado_inicial)