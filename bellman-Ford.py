import networkx as nx
import matplotlib.pyplot as plt

def dessiner_graphe(graphe, positions, distances, aretes_surlignees=[]):
    """
    Dessine le graphe avec les distances des nœuds et les arêtes surlignées.
    
    :param graphe: Le graphe à dessiner.
    :param positions: Un dictionnaire des positions des nœuds.
    :param distances: Un dictionnaire des distances des nœuds par rapport à la source.
    :param aretes_surlignees: Une liste des arêtes à surligner (par défaut, vide).
    """
    plt.figure(figsize=(8, 6))
    
    # Récupérer les arêtes et leurs poids
    aretes = graphe.edges(data=True)
    labels_aretes = {(u, v): d['weight'] for u, v, d in aretes}
    
    # Définir les couleurs des nœuds en fonction de leur distance
    couleurs_noeuds = ['lightgreen' if distances[n] < float('inf') else 'lightblue' for n in graphe.nodes]
    
    # Dessiner le graphe
    nx.draw(graphe, positions, with_labels=True, node_color=couleurs_noeuds, edge_color='gray', node_size=1000, font_size=12)
    nx.draw_networkx_edge_labels(graphe, positions, edge_labels=labels_aretes, font_size=10)
    
    # Surligner les arêtes spécifiées
    if aretes_surlignees:
        nx.draw_networkx_edges(graphe, positions, edgelist=aretes_surlignees, edge_color='r', width=2)
    
    # Ajouter les distances près des nœuds
    positions_decalées = {n: (x, y + 0.08) for n, (x, y) in positions.items()}  # Décalage vers le haut
    labels_distances = {n: f"{distances[n]}" if distances[n] < float('inf') else "" for n in graphe.nodes}
    nx.draw_networkx_labels(graphe, positions_decalées, labels=labels_distances, font_color='black', font_size=10, font_weight='bold', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    # Ajouter les ∞ pour les distances infinies
    labels_infini = {n: "∞" for n in graphe.nodes if distances[n] == float('inf')}
    positions_infini = {n: (x, y + 0.15) for n, (x, y) in positions.items()}  # Décalage plus haut
    nx.draw_networkx_labels(graphe, positions_infini, labels=labels_infini, font_color='red', font_size=12, font_weight='bold', bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    plt.title("Visualisation de l'algorithme de Bellman-Ford")
    plt.show()

def bellman_ford(graphe, source):
    """
    Applique l'algorithme de Bellman-Ford pour trouver les plus courts chemins depuis un nœud source.
    
    :param graphe: Une liste d'arêtes pondérées sous forme de tuples (u, v, poids).
    :param source: Le nœud source.
    :return: Un dictionnaire des distances des nœuds par rapport à la source.
    """
    # Créer un graphe orienté
    G = nx.DiGraph()
    G.add_weighted_edges_from(graphe)
    
    # Calculer les positions des nœuds pour le dessin
    positions = nx.spring_layout(G, k=3)  # Augmentation de l'espacement entre les nœuds
    
    # Initialiser les distances
    noeuds = list(G.nodes)
    distances = {noeud: float('inf') for noeud in noeuds}
    distances[source] = 0
    
    # Dessiner le graphe initial
    dessiner_graphe(G, positions, distances)
    
    # Appliquer l'algorithme de Bellman-Ford
    for _ in range(len(noeuds) - 1):
        for u, v, data in G.edges(data=True):
            poids = data['weight']
            if distances[u] + poids < distances[v]:
                distances[v] = distances[u] + poids
                dessiner_graphe(G, positions, distances, aretes_surlignees=[(u, v)])
    
    # Vérifier la présence de cycles de poids négatifs
    for u, v, data in G.edges(data=True):
        if distances[u] + data['weight'] < distances[v]:
            print("Le graphe contient un cycle de poids négatif")
            return None
    
    return distances

# Exemple d'utilisation
graphe = [(0, 1, 4), (0, 2, 3), (1, 2, -2), (2, 3, 2), (3, 1, -6)]
source = 0
distances = bellman_ford(graphe, source)
if distances:
    print("Distances finales:", distances)