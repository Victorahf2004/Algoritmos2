import networkx as nx

class Vertice:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.index = None

    def coords(self):
        return f'({self.x}, {self.y}), index: {self.index}'

class Aresta:
    def __init__(self, pInicio, pFinal):
        self.pInicio = pInicio
        self.pFinal = pFinal
        self.a1 = pFinal.x - pInicio.x
        self.a2 = pFinal.y - pInicio.y
    
    def imprimirPontos(self):
        return (f'Ponto de início: {self.pInicio.coords()}, Ponto final: {self.pFinal.coords()}, Componentes a1:{self.a1}, a2:{self.a2}, Vetor: ({self.a1}, {self.a2})')

class Grafo:
    def __init__(self):
        self.graph = nx.Graph()
        self.vertices = []
        self.arestas = []
    
    def adicionar_vertice(self, v):
        idx = len(self.vertices)
        v.index = idx
        self.vertices.append(v)
        self.graph.add_node(idx, pos=(v.x, v.y), color = None)
    
    def adicionar_aresta(self, ar):
        self.arestas.append(ar)
        self.graph.add_edge(ar.pInicio.index, ar.pFinal.index)

def mudancaDirecao3Pontos(ar1, ar2):
    """Determina a direção da mudança entre três pontos

    Args:
        ar1 (Aresta): Primeira aresta com propriedades pInicio e pFinal
        ar2 (Aresta): Segunda aresta com propriedades pInicio e pFinal

    Returns:
        str: Indica a direção da mudança ('horario', 'anti-horário' ou 'colinear')
    """
    # Vetor representando a primeira aresta
    vet1 = ar1
    # Vetor representando a segunda aresta, criado a partir dos pontos inicial da primeira e final da segunda
    vet2 = Aresta(ar1.pInicio, ar2.pFinal)
    
    # Coordenadas dos vetores
    a1 = vet1.a1
    a2 = vet1.a2
    b1 = vet2.a1
    b2 = vet2.a2
    
    # Calcula o determinante para determinar a direção
    a1b2 = a1 * b2
    b1a2 = b1 * a2
    c = a1b2 - b1a2
    
    # Determina a direção com base no valor do determinante
    direcao = ''
    if c < 0:
        direcao = 'horario'
    elif c > 0:
        direcao = 'anti-horário'
    else:
        direcao = 'colinear'
    
    return direcao

def pontoEstaNoTriangulo(p, ar1, ar2):
    """Verifica se um ponto está dentro do triângulo contendo o ponto p e as arestas ar1 e ar2.

    Args:
        p (Ponto): Ponto a ser verificado, com propriedades x e y
        ar1 (Segmento): Primeiro segmento de reta com propriedades pInicio e pFinal, onde cada um tem propriedades x e y
        ar2 (Segmento): Segundo segmento de reta com propriedades pInicio e pFinal, onde cada um tem propriedades x e y

    Returns:
        bool: True se o ponto p está dentro do triângulo, False caso contrário
    """
    def orientacao(p1, p2, p3):
        # Função auxiliar que retorna um valor numérico que pode ser positivo, negativo ou zero, dependendo da disposição dos três pontos.
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    a = ar1.pInicio
    b = ar1.pFinal
    c = ar2.pFinal

    d1 = orientacao(p, a, b)
    d2 = orientacao(p, b, c)
    d3 = orientacao(p, c, a)

    detNegativo = (d1 < 0) or (d2 < 0) or (d3 < 0)
    detPositivo = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (detNegativo and detPositivo)


def triangulacao(grafo, estagiosPoligono, instancias):
    """Função de implementação do algoritmo de Ear Clipping

    Args:
        grafo (Grafo): Grafo da estrutura de dados própria desse código
        estagiosPoligono (list): Lista com listas de pontos, indicando 
                               os pontos em cada frame para animação
        instancias (list): Lista para armazenar os índices das iterações para animação

    Returns:
        tuple: Contém o grafo atualizado, a lista de triângulos formados,
               os estágios do polígono para animação e as instâncias das iterações
    """
    # Inicialização das listas de vértices e arestas do grafo
    removed_vertices = [[]]
    
    vertices = list(grafo.vertices)
    arTriangulacao = list(grafo.arestas)
    triangulos = []
    tamanho = len(vertices)
    aresta = 0
    arestaProx = aresta + 1

    # Inicialização de variáveis para a animação
    teveOrelha = False
    y = 0
    verticesAnimacao = list(grafo.vertices)
    verticesAnimacao.append(verticesAnimacao[0])

    # Loop principal da triangulação enquanto houver mais de 3 vértices
    while tamanho > 3:
        teveOrelha = False
        pontoContido = False

        vertices2 = []
        ar1 = arTriangulacao[aresta].pInicio
        ar2 = arTriangulacao[arestaProx].pInicio
        ar3 = arTriangulacao[arestaProx].pFinal

        # Filtra os vértices que não são parte do triângulo atual
        for ver in vertices:
            if (((ver.x == ar1.x) and (ver.y == ar1.y)) and (ver.index == ar1.index)):
                continue
            elif (((ver.x == ar2.x) and (ver.y == ar2.y)) and (ver.index == ar2.index)):
                continue
            elif (((ver.x == ar3.x) and (ver.y == ar3.y)) and (ver.index == ar3.index)):
                continue
            else:
                vertices2.append(ver)

        # Verifica se algum vértice está contido no triângulo atual
        for v in vertices2:
            var = pontoEstaNoTriangulo(v, arTriangulacao[aresta], arTriangulacao[arestaProx])
            if var:
                pontoContido = True
                break

        # Verifica a direção dos pontos para determinar se é uma "orelha"
        direcao = mudancaDirecao3Pontos(arTriangulacao[aresta], arTriangulacao[arestaProx])
        if (direcao == 'anti-horário') and pontoContido is False:
            # Se for uma "orelha", realiza o corte
            to_remove  = removed_vertices[-1].copy()
            pInicio = arTriangulacao[aresta].pInicio
            pFinal = arTriangulacao[arestaProx].pFinal
            vertices.remove(arTriangulacao[aresta].pFinal)
            novaAresta = Aresta(pInicio, pFinal)
            novoTriangulo = (pInicio.index, arTriangulacao[aresta].pFinal.index, arTriangulacao[arestaProx].pFinal.index)
            triangulos.append(novoTriangulo)
            grafo.adicionar_aresta(novaAresta)

            # Atualiza a animação com os novos vértices
            verticesAnimacao.append(pFinal)
            vAnimacao = list(map(lambda P: (P.x, P.y), verticesAnimacao))
            estagiosPoligono.append(vAnimacao)
            
            to_remove.append((arTriangulacao[aresta].pFinal.x,arTriangulacao[aresta].pFinal.y))
            
            teveOrelha = True
            y += 1
            y2 = str(y)
            instancias.append(y2)

            # Atualiza as arestas após o corte
            arTriangulacao.insert(arestaProx, novaAresta)
            del arTriangulacao[arestaProx + 1]
            del arTriangulacao[aresta]
            tamanho = len(vertices)
            
            removed_vertices.append(to_remove)

        # Avança para a próxima aresta
        aresta += 1
        if aresta > tamanho - 1:
            aresta = 0
        arestaProx = aresta + 1
        if arestaProx > tamanho - 1:
            arestaProx = 0

        # Se não houve orelha, atualiza a animação com o próximo ponto
        if teveOrelha is False:
            y += 1
            verticesAnimacao.append(ar2)
            y2 = str(y)
            instancias.append(y2)
            vAnimacao = list(map(lambda P: (P.x, P.y), verticesAnimacao))
            estagiosPoligono.append(vAnimacao)
            
            removed_vertices.append(removed_vertices[-1])

    # Adiciona o último triângulo restante
    novoTriangulo = (arTriangulacao[0].pInicio.index, arTriangulacao[0].pFinal.index, arTriangulacao[1].pFinal.index)
    triangulos.append(novoTriangulo)
    y += 1
    y2 = str(y)
    instancias.append(y2)

    return (grafo, triangulos, estagiosPoligono, instancias, removed_vertices)



def colorirTriangulos(graph, triangulos, i):
    """Função para colorir os triângulos de um grafo

    Args:
        graph (networkx.Graph): Grafo que representa os triângulos
        triangulos (list): Lista de triângulos, onde cada triângulo é representado por uma tupla de três vértices
        i (int): Índice do triângulo atual a ser colorido

    Returns:
        tuple: Grafo atualizado com as cores dos nós e a lista de cores no estágio atual
    """
    cores = ['red', 'yellow', 'green']
    
    # Se for o primeiro triângulo, colore os três vértices com cores diferentes
    if i == 0:
        p1, p2, p3 = triangulos[i]
        graph.nodes[p1]['color'] = cores[0]
        graph.nodes[p2]['color'] = cores[1]
        graph.nodes[p3]['color'] = cores[2]
        estadoAtual = list(nx.get_node_attributes(graph, 'color').values())
        return graph, estadoAtual

    # Dicionário para armazenar os vértices já coloridos
    jaColoridos = dict()
    ponto = 0

    # Verifica quais vértices do triângulo já estão coloridos
    for p in triangulos[i]:
        if graph.nodes[p]['color'] != None:
            jaColoridos[p] = graph.nodes[p]['color']
        else:
            ponto = p

    # Determina a cor disponível que não está sendo usada pelos vértices adjacentes
    aColorir = list(set(cores) - (set(jaColoridos.values()) & set(cores)))[0]
    graph.nodes[ponto]['color'] = aColorir

    # Captura o estado atual das cores dos nós do grafo
    estadoAtual = list(nx.get_node_attributes(graph, 'color').values())
    return graph, estadoAtual