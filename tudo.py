import matplotlib.pyplot as plt
import networkx as nx

# seu vertice
class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.index = None

    def coords(self):
        return f'({self.x}, {self.y})'

# sua aresta
class Vector:
    def __init__(self, pInicio, pFinal):
        self.pInicio = pInicio
        self.pFinal = pFinal
        self.a1 = pFinal.x - pInicio.x
        self.a2 = pFinal.y - pInicio.y
    
    def imprimirPontos(self):
        print(f'Ponto de início: {self.pInicio.coords()}')
        print(f'Ponto final: {self.pFinal.coords()}')
        print(f'Componentes a1:{self.a1}, a2:{self.a2}')
        print(f'Vetor: ({self.a1}, {self.a2})')

class Grafo:
    def __init__(self):
        self.graph = nx.Graph()
        self.vertices = []
        self.arestas = []
    
    def adicionar_vertice(self, v):
        idx = len(self.vertices)
        v.index = idx
        self.vertices.append(v)
        self.graph.add_node(idx, pos=(v.x, v.y))
    
    def adicionar_aresta(self, ar):
        self.arestas.append(ar)
        self.graph.add_edge(ar.pInicio.index, ar.pFinal.index)

def mudancaDirecao3Pontos(ar1, ar2):
    vet1 = ar1
    vet2 = Vector(ar1.pInicio, ar2.pFinal)
    a1 = vet1.a1
    a2 = vet1.a2
    b1 = vet2.a1
    b2 = vet2.a2
    a1b2 = a1 * b2
    b1a2 = b1 * a2
    c = a1b2 - b1a2
    direcao = ''
    if c > 0:
        direcao = 'horario'
        print('Seguindo p0, p1, p2, tem sentido horário')
    elif c < 0:
        direcao = 'anti-horário'
        print('Seguindo p0, p1, p2, tem sentido anti-horário')
    else:
        direcao = 'colinear'
        print('P0, p1 e p2 são colineares')
    return direcao

def isPointInTriangle(p, a, b, c):
    # Calcular a área do triângulo original ABC usando a fórmula do determinante
    area_abc = abs((b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y))
    
    # Calcular as áreas dos triângulos menores PAB, PBC e PCA usando a mesma fórmula
    area_pab = abs((a.x - p.x) * (b.y - p.y) - (b.x - p.x) * (a.y - p.y))
    area_pbc = abs((b.x - p.x) * (c.y - p.y) - (c.x - p.x) * (b.y - p.y))
    area_pca = abs((c.x - p.x) * (a.y - p.y) - (a.x - p.x) * (c.y - p.y))
    
    # Verificar se a soma das áreas dos triângulos menores é igual à área do triângulo original
    var = (area_pab + area_pbc + area_pca) == area_abc
    print(f'O valor de var é: {var}')
    return var
# Função para plotar o polígono customizado
def plot_custom_polygon(G, vertices, arestas):
    fig, ax = plt.subplots()
    # Pega as posições dos nós
    pos = nx.get_node_attributes(G, 'pos')

    # Desenha o grafo
    nx.draw(G, pos, with_labels=True, node_color='cyan', edge_color='r', node_size=500, font_size=12, font_color='black')

    # Desenhar apenas os segmentos de arestas definidos
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

v1 = Ponto(0, 0)
v2 = Ponto(0, 3)
v3 = Ponto(4, 3)
v4 = Ponto(10, 20)
vertices = [v1, v2, v3, v4]
G = Grafo()
for v in vertices:
    G.adicionar_vertice(v)

ar1 = Vector(v1, v2)
ar2 = Vector(v2, v3)
# ar3 = Vector(v3, v4)
ar4 = Vector(v3, v1)
arestas = [ar1, ar2, ar4]
for aresta in arestas:
    G.adicionar_aresta(aresta)
# arestasGrafo = G.arestas
# tamanho = len(arestasGrafo)-1
# for par in range(tamanho):
#     print(f'vertices: ({arestasGrafo[par].pInicio.index}, {arestasGrafo[par].pFinal.index}), vertices: ({arestasGrafo[par+1].pInicio.index}, {arestasGrafo[par+1].pFinal.index})')
#     mudancaDirecao3Pontos(arestasGrafo[par], arestasGrafo[par+1])
#     print('Fim')
# print(f'vertices: ({arestasGrafo[-1].pInicio.index}, {arestasGrafo[-1].pFinal.index}), vertices: ({arestasGrafo[0].pInicio.index}, {arestasGrafo[0].pFinal.index})')
# mudancaDirecao3Pontos(arestasGrafo[-1], arestasGrafo[0])
# print('Fim')
# Chama a função para plotar o polígono
isPointInTriangle(v4, v1, v2, v3)
plot_custom_polygon(G.graph, vertices, arestas)