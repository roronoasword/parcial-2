import networkx as nx
import matplotlib.pyplot as plt

YO = "Angelo"

# ---------- Datos: lista de aristas por comunidad ----------
familia = ["Mamá", "Papá", "Hermano", "Abuelo", "Tía", "Primo"]
barrio = ["Esteban", "Nico", "Brayan", "Carlos", "Yeison"]
uni = ["Karen", "Mateo", "Isabella", "Julián", "Paula"]

grupo_de = {}
for g, lista in (("Familia", familia), ("Barrio", barrio), ("Universidad", uni)):
    for p in lista:
        grupo_de[p] = g

lazos_familia = [("Mamá", "Papá"), ("Mamá", "Hermano"), ("Papá", "Hermano"),
                 ("Mamá", "Abuelo"), ("Abuelo", "Tía"), ("Tía", "Primo"),
                 ("Papá", "Tía")]
lazos_barrio = [("Esteban", "Nico"), ("Nico", "Brayan"), ("Brayan", "Carlos"),
                ("Carlos", "Yeison"), ("Esteban", "Yeison"), ("Nico", "Carlos")]
lazos_uni = [("Karen", "Mateo"), ("Mateo", "Isabella"), ("Isabella", "Julián"),
             ("Julián", "Paula"), ("Karen", "Paula"), ("Mateo", "Julián")]
lazos_cruzados = [("Hermano", "Karen"), ("Primo", "Esteban"), ("Yeison", "Paula")]

# ---------- Estilo por grupo ----------
estilo = {
    "Familia":     {"color": "#ff6b9d", "forma": "s"},   # cuadrado
    "Barrio":      {"color": "#4ecdc4", "forma": "h"},   # hexágono
    "Universidad": {"color": "#ffd166", "forma": "D"},   # rombo
}

# ---------- Grafo ----------
G = nx.Graph()
G.add_node(YO)
for persona in grupo_de:
    G.add_edge(YO, persona)
G.add_edges_from(lazos_familia + lazos_barrio + lazos_uni + lazos_cruzados)

# ---------- Layout: spring con Angelo fijo en el centro ----------
semilla = {YO: (0, 0)}
sectores = {"Familia": (-1.6, 0.9), "Barrio": (1.6, 0.9), "Universidad": (0, -1.7)}
for g, (cx, cy) in sectores.items():
    miembros = [p for p, gr in grupo_de.items() if gr == g]
    for i, p in enumerate(miembros):
        semilla[p] = (cx + 0.15 * i, cy + 0.1 * i)
pos = nx.spring_layout(G, pos=semilla, fixed=[YO], k=0.9, iterations=300, seed=3)

# ---------- Dibujo ----------
fig, ax = plt.subplots(figsize=(12, 9), facecolor="#1b1b2f")
ax.set_facecolor("#1b1b2f")

for u, v in G.edges():
    if YO in (u, v):
        color, ancho, estilo_l, alfa = "#8888aa", 0.8, (0, (4, 4)), 0.6
    elif grupo_de[u] == grupo_de[v]:
        color, ancho, estilo_l, alfa = estilo[grupo_de[u]]["color"], 2.4, "-", 0.9
    else:
        color, ancho, estilo_l, alfa = "#ffffff", 2.0, (0, (1, 2)), 0.9
    nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=color,
                           width=ancho, style=estilo_l, alpha=alfa, ax=ax)

for g, est in estilo.items():
    nodos = [p for p, gr in grupo_de.items() if gr == g]
    tam = [700 + 350 * G.degree(n) for n in nodos]          # tamaño según conexiones
    nx.draw_networkx_nodes(G, pos, nodelist=nodos, node_color=est["color"],
                           node_shape=est["forma"], node_size=tam,
                           edgecolors="white", linewidths=1.5, ax=ax, label=g)

nx.draw_networkx_nodes(G, pos, nodelist=[YO], node_color="#ff4d4d", node_shape="*",
                       node_size=3800, edgecolors="white", linewidths=2, ax=ax, label=YO)

# Etiquetas con caja oscura para que siempre se lean
etiquetas = {n: n for n in G}
nx.draw_networkx_labels(G, pos, labels=etiquetas, font_size=9, font_color="white",
                        font_weight="bold", ax=ax,
                        bbox=dict(boxstyle="round,pad=0.25", fc="#1b1b2f", ec="none", alpha=0.85))

# Persona más conectada (sin contar a Angelo)
cent = nx.degree_centrality(G)
top = max((n for n in G if n != YO), key=cent.get)
ax.text(0.5, -0.04, f"Más conectado/a después de {YO}: {top} ({G.degree(top)} conexiones)",
        transform=ax.transAxes, ha="center", color="white", fontsize=11)

leg = ax.legend(loc="upper right", labelcolor="white", facecolor="#26264a",
                edgecolor="none", markerscale=0.4, fontsize=10)
ax.set_title(f"Mi red social · {YO}", color="white", fontsize=18, fontweight="bold")
ax.axis("off")
plt.tight_layout()
plt.show()