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
    #arTriangulacao é a cópia do vetor de arestas do grafo sobre a qual vou ir tirando e colocando novas arestas
    arTriangulacao = list(grafo.arestas)
    # arTriangulacao2 = arTriangulacao[::-1]
    # arTriangulacao = arTriangulacao2
    triangulos = []
    tamanho = len(vertices)
    aresta = 0
    arestaProx = aresta + 1
    while tamanho > 3:
        #print(f'Os vertices são {vertices}')
        #print(f'O tamanho é: {tamanho}')
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

## SIMPLE POLIGONS


# texto = '20 15428587209/1073741824 7213347949/1073741824 7903328829/1073741824 9829493019/1073741824 10733782533/1073741824 363880747/33554432 574699917/536870912 2855902701/268435456 -492455109/268435456 5669060337/536870912 -2250838011/1073741824 8736809679/1073741824 -1132780785/536870912 8086671779/1073741824 180136245/134217728 4040971139/1073741824 -194992041/67108864 99833389/67108864 -1070193633/536870912 2085885359/1073741824 -400440459/1073741824 1184113187/536870912 2764017039/536870912 939911471/268435456 6907239897/1073741824 2343713279/1073741824 9874707999/1073741824 1184716257/536870912 3304139745/536870912 3895709217/536870912 455759277/268435456 19180627/2097152 3464502989623856363/576460752303423488 2488545801/268435456 198770163/16777216 6517982929/1073741824 5018713419/536870912 56469663/8388608 2714027577/268435456 1076073767/536870912'
# texto = '20 -162759849/134217728 9651413259/1073741824 -2326417401/1073741824 357701181/268435456 388876515/1073741824 588629271/268435456 2856185517/536870912 1186983947/536870912 -691702413/536870912 1347803389/1073741824 -1032695049/1073741824 1210426599/1073741824 12210360837/1073741824 1373881799/1073741824 110683412153899889903/18446744073709551616 1861727379/1073741824 171707163/16777216 1521168849/1073741824 3850453347/268435456 930707763/134217728 14552525805/1073741824 2881646581/268435456 502543995/1073741824 1445901523/134217728 2332172847/536870912 8634224829/1073741824 6717754203/1073741824 2454369331/268435456 1274094327/134217728 8346619259/1073741824 12922609839/1073741824 137029701/16777216 11268454803/1073741824 6804140369/1073741824 436403247/67108864 2520940707/536870912 6953893899/1073741824 1451534001/268435456 -234450609/134217728 1375821957/536870912'
# texto = '20 3592015683/1073741824 5532366569/1073741824 2453309301/536870912 4761091819/1073741824 3211528803/1073741824 2340188827/536870912 -1770460581/1073741824 6382988039/1073741824 3799076853/536870912 1252239969/1073741824 3776364885/536870912 889823067/536870912 9134764899/1073741824 1962279917/536870912 14076368439/1073741824 5857617709/1073741824 13580021103/1073741824 8378414759/1073741824 109069021105797391/18014398509481984 2111614231/268435456 1923177315/536870912 10658260409/1073741824 7660655985/536870912 10550497089/1073741824 5281756977/536870912 88116943/8388608 29621289/33554432 1436426843/134217728 2247184479/536870912 2053043041/268435456 11489698941/1073741824 1724541931/268435456 1813953021/268435456 1826284497/536870912 3870720159/1073741824 3512750857/536870912 3173354061/1073741824 7363784119/1073741824 -1143823281/536870912 294786017/33554432'
# texto = '20 7 3 7 5 8 5 8 4 9 4 9 7 4 7 4 10 2 10 2 9 1 9 1 8 3 8 3 6 5 6 5 1 6 1 6 2 10 2 10 3'
# texto = 'X 0 0 0 3 4 3 4 0'

##

##ORTOGONAIS


# texto = '20 2/1 5/1 2/1 6/1 9/1 6/1 9/1 7/1 8/1 7/1 8/1 9/1 6/1 9/1 6/1 8/1 4/1 8/1 4/1 10/1 1/1 10/1 1/1 4/1 3/1 4/1 3/1 1/1 5/1 1/1 5/1 2/1 7/1 2/1 7/1 3/1 10/1 3/1 10/1 5/1'
# texto = '20 8/1 9/1 8/1 10/1 7/1 10/1 7/1 7/1 5/1 7/1 5/1 8/1 1/1 8/1 1/1 4/1 2/1 4/1 2/1 1/1 3/1 1/1 3/1 6/1 6/1 6/1 6/1 5/1 4/1 5/1 4/1 2/1 9/1 2/1 9/1 3/1 10/1 3/1 10/1 9/1'
# texto = '20 5/1 1/1 7/1 1/1 7/1 2/1 10/1 2/1 10/1 10/1 8/1 10/1 8/1 8/1 6/1 8/1 6/1 6/1 4/1 6/1 4/1 9/1 3/1 9/1 3/1 7/1 1/1 7/1 1/1 5/1 2/1 5/1 2/1 4/1 9/1 4/1 9/1 3/1 5/1 3/1'


##COMPLETE VON KOCH

# texto = '20 1/1 1/1 34/1 1/1 34/1 -95/4 67/1 -95/4 67/1 1/1 100/1 1/1 100/1 34/1 499/4 34/1 499/4 67/1 100/1 67/1 100/1 100/1 67/1 100/1 67/1 499/4 34/1 499/4 34/1 100/1 1/1 100/1 1/1 67/1 -95/4 67/1 -95/4 34/1 1/1 34/1'
# texto = '100 1/1 1/1 12/1 1/1 12/1 -29/4 23/1 -29/4 23/1 1/1 34/1 1/1 34/1 -29/4 445/16 -29/4 445/16 -31/2 34/1 -31/2 34/1 -95/4 45/1 -95/4 45/1 -32/1 56/1 -32/1 56/1 -95/4 67/1 -95/4 67/1 -31/2 1171/16 -31/2 1171/16 -29/4 67/1 -29/4 67/1 1/1 78/1 1/1 78/1 -29/4 89/1 -29/4 89/1 1/1 100/1 1/1 100/1 12/1 433/4 12/1 433/4 23/1 100/1 23/1 100/1 34/1 433/4 34/1 433/4 445/16 233/2 445/16 233/2 34/1 499/4 34/1 499/4 45/1 133/1 45/1 133/1 56/1 499/4 56/1 499/4 67/1 233/2 67/1 233/2 1171/16 433/4 1171/16 433/4 67/1 100/1 67/1 100/1 78/1 433/4 78/1 433/4 89/1 100/1 89/1 100/1 100/1 89/1 100/1 89/1 433/4 78/1 433/4 78/1 100/1 67/1 100/1 67/1 433/4 1171/16 433/4 1171/16 233/2 67/1 233/2 67/1 499/4 56/1 499/4 56/1 133/1 45/1 133/1 45/1 499/4 34/1 499/4 34/1 233/2 445/16 233/2 445/16 433/4 34/1 433/4 34/1 100/1 23/1 100/1 23/1 433/4 12/1 433/4 12/1 100/1 1/1 100/1 1/1 89/1 -29/4 89/1 -29/4 78/1 1/1 78/1 1/1 67/1 -29/4 67/1 -29/4 1171/16 -31/2 1171/16 -31/2 67/1 -95/4 67/1 -95/4 56/1 -32/1 56/1 -32/1 45/1 -95/4 45/1 -95/4 34/1 -31/2 34/1 -31/2 445/16 -29/4 445/16 -29/4 34/1 1/1 34/1 1/1 23/1 -29/4 23/1 -29/4 12/1 1/1 12/1'
# texto = '500 1/1 1/1 14/3 1/1 14/3 -7/4 25/3 -7/4 25/3 1/1 12/1 1/1 12/1 -7/4 159/16 -7/4 159/16 -9/2 12/1 -9/2 12/1 -29/4 47/3 -29/4 47/3 -10/1 58/3 -10/1 58/3 -29/4 23/1 -29/4 23/1 -9/2 401/16 -9/2 401/16 -7/4 23/1 -7/4 23/1 1/1 80/3 1/1 80/3 -7/4 91/3 -7/4 91/3 1/1 34/1 1/1 34/1 -7/4 511/16 -7/4 511/16 -9/2 34/1 -9/2 34/1 -29/4 511/16 -29/4 511/16 -365/64 239/8 -365/64 239/8 -29/4 445/16 -29/4 445/16 -10/1 103/4 -10/1 103/4 -51/4 445/16 -51/4 445/16 -31/2 239/8 -31/2 239/8 -1091/64 511/16 -1091/64 511/16 -31/2 34/1 -31/2 34/1 -73/4 511/16 -73/4 511/16 -21/1 34/1 -21/1 34/1 -95/4 113/3 -95/4 113/3 -53/2 124/3 -53/2 124/3 -95/4 45/1 -95/4 45/1 -53/2 687/16 -53/2 687/16 -117/4 45/1 -117/4 45/1 -32/1 146/3 -32/1 146/3 -139/4 157/3 -139/4 157/3 -32/1 56/1 -32/1 56/1 -117/4 929/16 -117/4 929/16 -53/2 56/1 -53/2 56/1 -95/4 179/3 -95/4 179/3 -53/2 190/3 -53/2 190/3 -95/4 67/1 -95/4 67/1 -21/1 1105/16 -21/1 1105/16 -73/4 67/1 -73/4 67/1 -31/2 1105/16 -31/2 1105/16 -1091/64 569/8 -1091/64 569/8 -31/2 1171/16 -31/2 1171/16 -51/4 301/4 -51/4 301/4 -10/1 1171/16 -10/1 1171/16 -29/4 569/8 -29/4 569/8 -365/64 1105/16 -365/64 1105/16 -29/4 67/1 -29/4 67/1 -9/2 1105/16 -9/2 1105/16 -7/4 67/1 -7/4 67/1 1/1 212/3 1/1 212/3 -7/4 223/3 -7/4 223/3 1/1 78/1 1/1 78/1 -7/4 1215/16 -7/4 1215/16 -9/2 78/1 -9/2 78/1 -29/4 245/3 -29/4 245/3 -10/1 256/3 -10/1 256/3 -29/4 89/1 -29/4 89/1 -9/2 1457/16 -9/2 1457/16 -7/4 89/1 -7/4 89/1 1/1 278/3 1/1 278/3 -7/4 289/3 -7/4 289/3 1/1 100/1 1/1 100/1 14/3 411/4 14/3 411/4 25/3 100/1 25/3 100/1 12/1 411/4 12/1 411/4 159/16 211/2 159/16 211/2 12/1 433/4 12/1 433/4 47/3 111/1 47/3 111/1 58/3 433/4 58/3 433/4 23/1 211/2 23/1 211/2 401/16 411/4 401/16 411/4 23/1 100/1 23/1 100/1 80/3 411/4 80/3 411/4 91/3 100/1 91/3 100/1 34/1 411/4 34/1 411/4 511/16 211/2 511/16 211/2 34/1 433/4 34/1 433/4 511/16 6829/64 511/16 6829/64 239/8 433/4 239/8 433/4 445/16 111/1 445/16 111/1 103/4 455/4 103/4 455/4 445/16 233/2 445/16 233/2 239/8 7555/64 239/8 7555/64 511/16 233/2 511/16 233/2 34/1 477/4 34/1 477/4 511/16 122/1 511/16 122/1 34/1 499/4 34/1 499/4 113/3 255/2 113/3 255/2 124/3 499/4 124/3 499/4 45/1 255/2 45/1 255/2 687/16 521/4 687/16 521/4 45/1 133/1 45/1 133/1 146/3 543/4 146/3 543/4 157/3 133/1 157/3 133/1 56/1 521/4 56/1 521/4 929/16 255/2 929/16 255/2 56/1 499/4 56/1 499/4 179/3 255/2 179/3 255/2 190/3 499/4 190/3 499/4 67/1 122/1 67/1 122/1 1105/16 477/4 1105/16 477/4 67/1 233/2 67/1 233/2 1105/16 7555/64 1105/16 7555/64 569/8 233/2 569/8 233/2 1171/16 455/4 1171/16 455/4 301/4 111/1 301/4 111/1 1171/16 433/4 1171/16 433/4 569/8 6829/64 569/8 6829/64 1105/16 433/4 1105/16 433/4 67/1 211/2 67/1 211/2 1105/16 411/4 1105/16 411/4 67/1 100/1 67/1 100/1 212/3 411/4 212/3 411/4 223/3 100/1 223/3 100/1 78/1 411/4 78/1 411/4 1215/16 211/2 1215/16 211/2 78/1 433/4 78/1 433/4 245/3 111/1 245/3 111/1 256/3 433/4 256/3 433/4 89/1 211/2 89/1 211/2 1457/16 411/4 1457/16 411/4 89/1 100/1 89/1 100/1 278/3 411/4 278/3 411/4 289/3 100/1 289/3 100/1 100/1 289/3 100/1 289/3 411/4 278/3 411/4 278/3 100/1 89/1 100/1 89/1 411/4 1457/16 411/4 1457/16 211/2 89/1 211/2 89/1 433/4 256/3 433/4 256/3 111/1 245/3 111/1 245/3 433/4 78/1 433/4 78/1 211/2 1215/16 211/2 1215/16 411/4 78/1 411/4 78/1 100/1 223/3 100/1 223/3 411/4 212/3 411/4 212/3 100/1 67/1 100/1 67/1 411/4 1105/16 411/4 1105/16 211/2 67/1 211/2 67/1 433/4 1105/16 433/4 1105/16 6829/64 569/8 6829/64 569/8 433/4 1171/16 433/4 1171/16 111/1 301/4 111/1 301/4 455/4 1171/16 455/4 1171/16 233/2 569/8 233/2 569/8 7555/64 1105/16 7555/64 1105/16 233/2 67/1 233/2 67/1 477/4 1105/16 477/4 1105/16 122/1 67/1 122/1 67/1 499/4 190/3 499/4 190/3 255/2 179/3 255/2 179/3 499/4 56/1 499/4 56/1 255/2 929/16 255/2 929/16 521/4 56/1 521/4 56/1 133/1 157/3 133/1 157/3 543/4 146/3 543/4 146/3 133/1 45/1 133/1 45/1 521/4 687/16 521/4 687/16 255/2 45/1 255/2 45/1 499/4 124/3 499/4 124/3 255/2 113/3 255/2 113/3 499/4 34/1 499/4 34/1 122/1 511/16 122/1 511/16 477/4 34/1 477/4 34/1 233/2 511/16 233/2 511/16 7555/64 239/8 7555/64 239/8 233/2 445/16 233/2 445/16 455/4 103/4 455/4 103/4 111/1 445/16 111/1 445/16 433/4 239/8 433/4 239/8 6829/64 511/16 6829/64 511/16 433/4 34/1 433/4 34/1 211/2 511/16 211/2 511/16 411/4 34/1 411/4 34/1 100/1 91/3 100/1 91/3 411/4 80/3 411/4 80/3 100/1 23/1 100/1 23/1 411/4 401/16 411/4 401/16 211/2 23/1 211/2 23/1 433/4 58/3 433/4 58/3 111/1 47/3 111/1 47/3 433/4 12/1 433/4 12/1 211/2 159/16 211/2 159/16 411/4 12/1 411/4 12/1 100/1 25/3 100/1 25/3 411/4 14/3 411/4 14/3 100/1 1/1 100/1 1/1 289/3 -7/4 289/3 -7/4 278/3 1/1 278/3 1/1 89/1 -7/4 89/1 -7/4 1457/16 -9/2 1457/16 -9/2 89/1 -29/4 89/1 -29/4 256/3 -10/1 256/3 -10/1 245/3 -29/4 245/3 -29/4 78/1 -9/2 78/1 -9/2 1215/16 -7/4 1215/16 -7/4 78/1 1/1 78/1 1/1 223/3 -7/4 223/3 -7/4 212/3 1/1 212/3 1/1 67/1 -7/4 67/1 -7/4 1105/16 -9/2 1105/16 -9/2 67/1 -29/4 67/1 -29/4 1105/16 -365/64 1105/16 -365/64 569/8 -29/4 569/8 -29/4 1171/16 -10/1 1171/16 -10/1 301/4 -51/4 301/4 -51/4 1171/16 -31/2 1171/16 -31/2 569/8 -1091/64 569/8 -1091/64 1105/16 -31/2 1105/16 -31/2 67/1 -73/4 67/1 -73/4 1105/16 -21/1 1105/16 -21/1 67/1 -95/4 67/1 -95/4 190/3 -53/2 190/3 -53/2 179/3 -95/4 179/3 -95/4 56/1 -53/2 56/1 -53/2 929/16 -117/4 929/16 -117/4 56/1 -32/1 56/1 -32/1 157/3 -139/4 157/3 -139/4 146/3 -32/1 146/3 -32/1 45/1 -117/4 45/1 -117/4 687/16 -53/2 687/16 -53/2 45/1 -95/4 45/1 -95/4 124/3 -53/2 124/3 -53/2 113/3 -95/4 113/3 -95/4 34/1 -21/1 34/1 -21/1 511/16 -73/4 511/16 -73/4 34/1 -31/2 34/1 -31/2 511/16 -1091/64 511/16 -1091/64 239/8 -31/2 239/8 -31/2 445/16 -51/4 445/16 -51/4 103/4 -10/1 103/4 -10/1 445/16 -29/4 445/16 -29/4 239/8 -365/64 239/8 -365/64 511/16 -29/4 511/16 -29/4 34/1 -9/2 34/1 -9/2 511/16 -7/4 511/16 -7/4 34/1 1/1 34/1 1/1 91/3 -7/4 91/3 -7/4 80/3 1/1 80/3 1/1 23/1 -7/4 23/1 -7/4 401/16 -9/2 401/16 -9/2 23/1 -29/4 23/1 -29/4 58/3 -10/1 58/3 -10/1 47/3 -29/4 47/3 -29/4 12/1 -9/2 12/1 -9/2 159/16 -7/4 159/16 -7/4 12/1 1/1 12/1 1/1 25/3 -7/4 25/3 -7/4 14/3 1/1 14/3'

#RANDOM VON KOCH

# texto = '20 1/1 1/1 100/1 1/1 100/1 34/1 499/4 34/1 499/4 67/1 100/1 67/1 100/1 100/1 67/1 100/1 67/1 499/4 56/1 499/4 56/1 133/1 45/1 133/1 45/1 499/4 34/1 499/4 34/1 100/1 1/1 100/1 1/1 67/1 -95/4 67/1 -95/4 34/1 1/1 34/1'
# texto = '20 1/1 1/1 34/1 1/1 34/1 -95/4 67/1 -95/4 67/1 1/1 100/1 1/1 100/1 12/1 433/4 12/1 433/4 23/1 100/1 23/1 100/1 34/1 499/4 34/1 499/4 67/1 100/1 67/1 100/1 78/1 433/4 78/1 433/4 89/1 100/1 89/1 100/1 100/1 1/1 100/1'
# texto = '20 1/1 1/1 34/1 1/1 34/1 -29/4 445/16 -29/4 445/16 -31/2 34/1 -31/2 34/1 -95/4 67/1 -95/4 67/1 1/1 100/1 1/1 100/1 34/1 499/4 34/1 499/4 67/1 100/1 67/1 100/1 100/1 1/1 100/1 1/1 67/1 -95/4 67/1 -95/4 34/1 1/1 34/1'
'''
texto = '20 1/1 1/1 34/1 1/1 34/1 -29/4 445/16 -29/4 445/16 -31/2 34/1 -31/2 34/1 -95/4 67/1 -95/4 67/1 1/1 100/1 1/1 100/1 34/1 499/4 34/1 499/4 67/1 100/1 67/1 100/1 100/1 1/1 100/1 1/1 67/1 -95/4 67/1 -95/4 34/1 1/1 34/1'
lista = texto.split()
lista = lista[1:]
lista2 = []
for elem in lista:
    if '/' in elem:
        numerador, denominador = map(float, elem.split('/'))
        resultado = numerador / denominador
        lista2.append(resultado)
    else:
        elem2 = float(elem)
        lista2.append(elem2)
lista = lista2
pontos = []
for i in range(0, len(lista) - 1, 2):
  tupla = Vertice(lista[i], lista[i + 1])
  pontos.append(tupla)
G = Grafo()
for v in pontos:
    G.adicionar_vertice(v)

# print(pontos)
arestas = []

tamanho = len(pontos) - 1
for i in range(tamanho):
    ar = Aresta(pontos[i], pontos[i + 1])
    arestas.append(ar)

ar = Aresta(pontos[tamanho], pontos[0])
arestas.append(ar)

for aresta in arestas:
    G.adicionar_aresta(aresta)
(G, triangulos) = triangulacao(G)

for t in triangulos:
    print(f'Um triangulo é: {t}')
    print()
plot_custom_polygon(G.graph, pontos, arestas)

# v1 = Ponto(0, 0)
# v2 = Ponto(0, 3)
# v3 = Ponto(2, 5)
# v4 = Ponto(5, 6)
# v5 = Ponto(7, 5)
# v6 = Ponto(9, 3)
# v7 = Ponto(9, 0)
# v8 = Ponto(8, -3)
# v9 = Ponto(5, -5)
# v10 = Ponto(2, -5)
# v11 = Ponto(-1, -3)
# v12 = Ponto(-3, -1)
# v13 = Ponto(-4, 2)
# v14 = Ponto(-3, 4)
# v15 = Ponto(-1, 5)
# v16 = Ponto(2, 7)
# v17 = Ponto(5, 8)
# v18 = Ponto(8, 7)
# v19 = Ponto(10, 5)
# v20 = Ponto(10, 2)
# vertices = [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20]
# G = Grafo()
# for v in vertices:
#     G.adicionar_vertice(v)

# ar1 = Vector(v1, v2)
# ar2 = Vector(v2, v3)
# ar3 = Vector(v3, v4)
# ar4 = Vector(v4, v5)
# ar5 = Vector(v5, v6)
# ar6 = Vector(v6, v7)
# ar7 = Vector(v7, v8)
# ar8 = Vector(v8, v9)
# ar9 = Vector(v9, v10)
# ar10 = Vector(v10, v11)
# ar11 = Vector(v11, v12)
# ar12 = Vector(v12, v13)
# ar13 = Vector(v13, v14)
# ar14 = Vector(v14, v15)
# ar15 = Vector(v15, v16)
# ar16 = Vector(v16, v17)
# ar17 = Vector(v17, v18)
# ar18 = Vector(v18, v19)
# ar19 = Vector(v19, v20)
# ar20 = Vector(v20, v1)
# arestas = [ar1, ar2, ar3, ar4, ar5, ar6, ar7, ar8, ar9, ar10, ar11, ar12, ar13, ar14, ar15, ar16, ar17, ar18, ar19, ar20]
# for aresta in arestas:
#     G.adicionar_aresta(aresta)
# (G, triangulos) = triangulacao(G)
'''