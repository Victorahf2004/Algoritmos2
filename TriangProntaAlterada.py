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


def triangulacao(grafo, polygon_stages, intances):
    """Função de implementação do algoritmo de Ear Clipping

    Args:
        grafo (Grafo): Grafo da estrutura de dados própria desse código
        polygon_stages (list): Lista com listas de pontos, indicando 
                               os pontos em cada frame para animação
        intances (_type_): _description_

    Returns:
        _type_: _description_
    """
    #Inicalza com nada (GAB)
    removed_vertices = [[]]
    
    vertices = list(grafo.vertices)
    arTriangulacao = list(grafo.arestas)
    triangulos = []
    tamanho = len(vertices)
    aresta = 0
    arestaProx = aresta + 1
    ###
    teveOrelha = False
    y = 0
    verticesAnimacao = list(grafo.vertices)
    verticesAnimacao.append(verticesAnimacao[0])
    ###
    while tamanho > 3:
        ###
        teveOrelha = False
        pontoContido = False
        ###

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
            if var:
                pontoContido = True
                break
        direcao = mudancaDirecao3Pontos(arTriangulacao[aresta], arTriangulacao[arestaProx])
        if (direcao == 'anti-horário') and pontoContido is False:
            to_remove  = removed_vertices[-1].copy()
            pInicio = arTriangulacao[aresta].pInicio
            pFinal = arTriangulacao[arestaProx].pFinal
            vertices.remove(arTriangulacao[aresta].pFinal)
            
            # Adiciona vertices removidos(GAB)
            to_remove.append((arTriangulacao[aresta].pFinal.x,arTriangulacao[aresta].pFinal.y))
            
            nova_aresta = Aresta(pInicio, pFinal)
            novo_triangulo = (pInicio.index, arTriangulacao[aresta].pFinal.index, arTriangulacao[arestaProx].pFinal.index)
            triangulos.append(novo_triangulo)
            grafo.adicionar_aresta(nova_aresta)
            # ###

            verticesAnimacao.append(pFinal)
            vAnimacao = list(map(lambda P: (P.x,P.y), verticesAnimacao))
            polygon_stages.append(vAnimacao)
            teveOrelha = True
            y += 1
            y2 = str(y)
            intances.append(y2)

            # ###
            arTriangulacao.insert(arestaProx, nova_aresta)
            del arTriangulacao[arestaProx + 1]
            del arTriangulacao[aresta]
            tamanho = len(vertices)
            
            # Adiciona no Geral(GAB)
            removed_vertices.append(to_remove)
            
        aresta += 1
        if aresta > tamanho - 1:
            aresta = 0
        arestaProx = aresta + 1
        if arestaProx > tamanho - 1:
            arestaProx = 0
        # ###
        if teveOrelha is False:
            y += 1
            verticesAnimacao.append(ar2)
            y2 = str(y)
            intances.append(y2)
            vAnimacao = list(map(lambda P: (P.x,P.y), verticesAnimacao))
            polygon_stages.append(vAnimacao)
        # ###
    novo_triangulo = (arTriangulacao[0].pInicio.index, arTriangulacao[0].pFinal.index, arTriangulacao[1].pFinal.index)
    triangulos.append(novo_triangulo)
    y += 1
    y2 = str(y)
    intances.append(y2)
    return (grafo, triangulos, polygon_stages, intances, removed_vertices)


def color_triangle(graph, triangulos, i):
    colors = ['red', 'yellow', 'green']
    
    if i == 0:
        p1,p2,p3 = triangulos[i]
        graph.nodes[p1]['color'] = colors[0]
        graph.nodes[p2]['color'] = colors[1]
        graph.nodes[p3]['color'] = colors[2]
        actual_stage = (list(nx.get_node_attributes(graph,'color').values()))
        return graph, actual_stage

    ja_coloridos = dict()
    point = 0
    for p in triangulos[i]:
        if graph.nodes[p]['color'] != None:
            ja_coloridos[p] = graph.nodes[p]['color']
        else:
            point = p    
            
    to_color = list((set(colors) - (set(ja_coloridos.values()) & set(colors))))[0]
    graph.nodes[point]['color'] = to_color
    actual_stage = (list(nx.get_node_attributes(graph,'color').values()))
    return graph, actual_stage