import matplotlib.pyplot as plt
import networkx as nx

def criar_grafo(vertices, edges):
    # Cria um grafo
    G = nx.Graph()

    # Adiciona os vértices ao grafo
    for idx, vertex in enumerate(vertices):
        G.add_node(idx, pos=vertex)

    # Adiciona as arestas ao grafo
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    return G
def plot_custom_polygon(G):
    fig, ax = plt.subplots()
    # Pega as posições dos nós
    pos = nx.get_node_attributes(G, 'pos')

    # Desenha o grafo
    nx.draw(G, pos, with_labels=True, node_color='cyan', edge_color='r', node_size=500, font_size=12, font_color='black')

    # Preenche o interior do polígono
    polygon = plt.Polygon([vertices[v] for v in G.nodes], closed=True, fill=True, edgecolor='r', facecolor='cyan', alpha=0.5)
    ax.add_patch(polygon)

    # Ajusta os limites do gráfico
    ax.set_xlim(min(x for x, y in vertices) - 1, max(x for x, y in vertices) + 1)
    ax.set_ylim(min(y for x, y in vertices) - 1, max(y for x, y in vertices) + 1)
    ax.set_aspect('equal')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Custom Polygon')
    plt.grid(True)

    plt.show()

# Lista de vértices do polígono (exemplo)
vertices = [(1, 1), (4, 1), (4, 4), (1, 4)]

# Lista de arestas do polígono (exemplo)
edges = [(0, 1), (1, 2), (2, 3), (3, 0)]

G = criar_grafo(vertices, edges)
# Chama a função para plotar o polígono
plot_custom_polygon(G)