from gui import GraphGUI
import prim
import kruskal

grafo = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('C', 5), ('D', 10)],
    'C': [('A', 2), ('B', 5), ('D', 3), ('E', 4)],
    'D': [('B', 10), ('C', 3), ('E', 11), ('F', 2)],
    'E': [('C', 4), ('D', 11), ('F', 5)],
    'F': [('D', 2), ('E', 5)]
}

gui = GraphGUI(
    grafo=grafo,
    prim_func=prim.prim,
    kruskal_func=kruskal.kruskal,
)

gui.iniciar()
