import matplotlib.pyplot as plt
import networkx as nx
import math

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
    vet1 = ar1
    vet2 = Aresta(ar1.pInicio, ar2.pFinal)
    a1 = vet1.a1
    a2 = vet1.a2
    b1 = vet2.a1
    b2 = vet2.a2
    a1b2 = a1 * b2
    b1a2 = b1 * a2
    c = a1b2 - b1a2
    direcao = ''
    if c < 0:
        direcao = 'horario'
    elif c > 0:
        direcao = 'anti-horário'
    else:
        direcao = 'colinear'
    return direcao

def isPointInTriangle(p, ar1, ar2):
    def sign(p1, p2, p3):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)

    a = ar1.pInicio
    b = ar1.pFinal
    c = ar2.pFinal

    d1 = sign(p, a, b)
    d2 = sign(p, b, c)
    d3 = sign(p, c, a)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)

# Função para plotar o polígono
def plot_custom_polygon(G, vertices, arestas):
    fig, ax = plt.subplots()
    # Pega as posições dos nós
    pos = nx.get_node_attributes(G, 'pos')

    # Desenha o grafo
    nx.draw(G, pos, with_labels=True, node_color='cyan', edge_color='r', node_size=500, font_size=12, font_color='black')

    # Desenha apenas os segmentos de arestas definidos
    for ar in arestas:
        x_values = [ar.pInicio.x, ar.pFinal.x]
        y_values = [ar.pInicio.y, ar.pFinal.y]
        ax.plot(x_values, y_values, 'r-')

    # Ajusta os limites do gráfico
    ax.set_xlim(min(v.x for v in vertices) - 1, max(v.x for v in vertices) + 1)
    ax.set_ylim(min(v.y for v in vertices) - 1, max(v.y for v in vertices) + 1)
    ax.set_aspect('equal')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Custom Polygon')
    plt.grid(True)

    plt.show()

def triangulacao(grafo):
    vertices = list(grafo.vertices)
    arTriangulacao = list(grafo.arestas)
    triangulos = []
    tamanho = len(vertices)
    aresta = 0
    arestaProx = aresta + 1
    while tamanho > 3:
        pontoContido = False
        vertices2 = []
        ar1 = arTriangulacao[aresta].pInicio
        ar2 = arTriangulacao[arestaProx].pInicio
        ar3 = arTriangulacao[arestaProx].pFinal
        for ver in vertices:
            if (((ver.x == ar1.x) and (ver.y == ar1.y)) and (ver.index == ar1.index)):
                continue
            elif (((ver.x == ar2.x) and (ver.y == ar2.y)) and (ver.index == ar2.index)):
                continue
            elif (((ver.x == ar3.x) and (ver.y == ar3.y)) and (ver.index == ar3.index)):
                continue
            else:
                vertices2.append(ver)
        for v in vertices2:
            var = isPointInTriangle(v, arTriangulacao[aresta], arTriangulacao[arestaProx])
            # print(f'Var é: {var}')
            if var:
                pontoContido = True
                break
        direcao = mudancaDirecao3Pontos(arTriangulacao[aresta], arTriangulacao[arestaProx])
        if (direcao == 'anti-horário') and pontoContido is False:
            pInicio = arTriangulacao[aresta].pInicio
            pFinal = arTriangulacao[arestaProx].pFinal
            vertices.remove(arTriangulacao[aresta].pFinal)
            nova_aresta = Aresta(pInicio, pFinal)
            novo_triangulo = (pInicio.index, arTriangulacao[aresta].pFinal.index, arTriangulacao[arestaProx].pFinal.index)
            triangulos.append(novo_triangulo)
            grafo.adicionar_aresta(nova_aresta)
            arTriangulacao.insert(arestaProx, nova_aresta)
            del arTriangulacao[arestaProx + 1]
            del arTriangulacao[aresta]
            tamanho = len(vertices)
        aresta += 1
        if aresta > tamanho - 1:
            aresta = 0
        arestaProx = aresta + 1
        if arestaProx > tamanho - 1:
            arestaProx = 0
    novo_triangulo = (arTriangulacao[0].pInicio.index, arTriangulacao[0].pFinal.index, arTriangulacao[1].pFinal.index)
    triangulos.append(novo_triangulo)
    return (grafo, triangulos)