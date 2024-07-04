import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from shapely.geometry import Point, Polygon as ShapelyPolygon

def is_point_in_triangle(pt, v1, v2, v3):
    """Check if a point pt is inside the triangle formed by v1, v2, v3"""
    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0
    return ((b1 == b2) and (b2 == b3))

def sign(p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def ear_clipping_triangulation(vertices):
    """Ear clipping algorithm to triangulate a polygon"""
    if len(vertices) < 3:
        return []

    triangles = []
    v = vertices[:]
    
    while len(v) > 3:
        for i in range(len(v)):
            p1 = v[i]
            p2 = v[(i + 1) % len(v)]
            p3 = v[(i + 2) % len(v)]

            ear_found = True
            triangle = ShapelyPolygon([p1, p2, p3])

            if triangle.is_valid:
                for j in range(len(v)):
                    if j != i and j != (i + 1) % len(v) and j != (i + 2) % len(v):
                        point = Point(v[j])
                        if point.within(triangle):
                            ear_found = False
                            break

                if ear_found:
                    triangles.append([p1, p2, p3])
                    del v[(i + 1) % len(v)]
                    break

    triangles.append([v[0], v[1], v[2]])
    return triangles

def plot_polygon_with_triangulation(vertices, triangles):
    fig, ax = plt.subplots()
    polygon = Polygon(vertices, closed=True, fill=None, edgecolor='r')
    ax.add_patch(polygon)

    for triangle in triangles:
        t = Polygon(triangle, closed=True, fill=True, edgecolor='b', alpha=0.3)
        ax.add_patch(t)

    x, y = zip(*vertices)
    ax.plot(x, y, 'ro')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Polygon with Triangulation')
    plt.grid(True)
    plt.show()

# Exemplo de vértices do polígono
vertices = [(1, 1), (5, 1), (5, 5), (3, 3), (1, 5)]

# Triangulação usando o algoritmo Ear Clipping
triangles = ear_clipping_triangulation(vertices)

# Plotar o polígono com a triangulação
plot_polygon_with_triangulation(vertices, triangles)
