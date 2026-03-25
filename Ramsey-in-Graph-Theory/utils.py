import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import os
import random

def concentric_layout(groups, radii=None, scale_step=1.0):
    pos = {}
    for ring_index, group in enumerate(groups):
        if radii:
            radius = radii[ring_index]
        else:
            radius = (ring_index + 1) * scale_step
        for i, node in enumerate(group):
            angle = 2 * 3.14159 * i / len(group)
            pos[node] = (radius * __import__('math').cos(angle),
                         radius * __import__('math').sin(angle))
    return pos

    
def r_coloring_K_n(
    n,
    edge_coloring = None, 
    palette = None, 
    labels = None,
    node_color = "black",
    node_size = 500,
    font_size = 12,
    font_color = "white",
    width = 2.0,
    figsize = (6,6),
    with_labels = True,
    title = None,
    save_path = None,
    groups = None,
    scale_step = 1.0,
    radii=None
):
    G = nx.complete_graph(n)
    pos = nx.circular_layout(G)
    colors = palette or r_colors
    label_map = labels or {i : str(i) for i in G.nodes()}

    if groups:
        pos = concentric_layout(groups, radii=radii, scale_step=scale_step)
    else:
        pos = nx.circular_layout(G)
    
    if edge_coloring is None:
        edge_coloring = [list(G.edges())]
        
    fig, ax = plt.subplots(figsize=figsize)

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_color, node_size=node_size)
    
    if with_labels:
        nx.draw_networkx_labels(G, pos, ax=ax, labels=label_map, font_size=font_size, font_color=font_color)

    for color_class, color in zip(edge_coloring, colors):
        nx.draw_networkx_edges(
            G, pos, ax=ax,
            edgelist=list(color_class),
            edge_color=color,
            width=width,
        )

    ax.set_title(title or " ", fontsize=14)
    ax.axis("off")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path)
    else: 
        plt.show()

def monochromatic_triangle_check(partition):
    results = []
    for i, edge_set in enumerate(partition):
        for triple in combinations(edge_set,3):
            numbers = set()
            for pair in triple:
                numbers.update(pair)
            if len(numbers) == 3:
                results.append(triple)
    return(results)

def has_clique(vertices, coloring, color, size):
    if size == 0:
        return True
    if len(vertices) < size:
        return False
    v = next(iter(vertices))
    rest = vertices - {v}
    color_neighbors = frozenset(
        w for w in rest
        if coloring.get(_edge(v, w)) == color
    )
    if has_clique(color_neighbors, coloring, color, size - 1):
        return True
    return has_clique(rest, coloring, color, size)

def _edge(u, v):
    return (u, v) if u < v else (v, u)

def is_forbidden(u, v, color, coloring, n_clique):
    if n_clique <= 2:
        return False
    colored_with_u = {
        w for (a, b), c in coloring.items()
        if c == color and (a == u or b == u)
        for w in ([b] if a == u else [a])
    }
    colored_with_v = {
        w for (a, b), c in coloring.items()
        if c == color and (a == v or b == v)
        for w in ([b] if a == v else [a])
    }
    W = frozenset(colored_with_u & colored_with_v)

    return has_clique(W, coloring, color, n_clique - 2)

def count_cliques(vertices, coloring, color, size):
    if size == 0:
        return 1
    if len(vertices) < size:
        return 0
    v = next(iter(vertices))
    rest = vertices - {v}
    color_neighbors = frozenset(
        w for w in rest
        if coloring.get(_edge(v, w)) == color
    )
    return (count_cliques(color_neighbors, coloring, color, size - 1)
            + count_cliques(rest, coloring, color, size))

def make_edges_by_vertex(N):
    edges = []
    for i in range(N):
        for j in range(i):
            edges.append((j, i))
    return edges

COLOR_NAMES = ['Red', 'Blue', 'Green', 'Yellow', 'Magenta', 'Cyan']
