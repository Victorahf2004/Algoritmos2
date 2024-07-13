import plotly_express as px
import numpy as np

def det(p, q, r):
    """Return positive if p-q-r are clockwise, negative if counterclockwise, zero if collinear."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

def is_point_in_triangle(pt, v1, v2, v3):
    """Check if a point pt is inside the triangle v1v2v3."""
    d1 = det(pt, v1, v2)
    d2 = det(pt, v2, v3)
    d3 = det(pt, v3, v1)
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)

def is_ear(polygon, i):
    """Check if the vertex i forms an ear."""
    n = len(polygon)
    prev = polygon[(i-1) % n]
    curr = polygon[i]
    next = polygon[(i+1) % n]
    
    # Check if the triangle prev-curr-next is convex
    if det(prev, curr, next) >= 0:
        return False    

    # Check if any point in the polygon is inside the triangle prev-curr-next
    for j in range(n):
        if j == i or j == (i-1) % n or j == (i+1) % n:
            continue
        if is_point_in_triangle(polygon[j], prev, curr, next):
            return False

    return True

def triangulate_polygon(polygon):
    n = len(polygon)
    indices = list(range(n))
    triangles = []

    while len(indices) > 3:
        for i in range(len(indices)):
            if is_ear(polygon, indices[i]):
                ear = indices[i]
                prev = indices[(i-1) % len(indices)]
                next = indices[(i+1) % len(indices)]
                triangles.append((polygon[prev], polygon[ear], polygon[next]))
                indices.pop(i) #del indices[i]
                fig = px.line(x=np.array(polygon)[indices][:,0],y=np.array(polygon)[indices][:,1],markers=True)
                fig.update_traces(marker_size=10)
                fig.show()
                break

    triangles.append((polygon[indices[0]], polygon[indices[1]], polygon[indices[2]]))
    return triangles