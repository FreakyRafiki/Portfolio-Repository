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

