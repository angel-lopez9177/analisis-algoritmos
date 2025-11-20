import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt

class GraphGUI:

    def __init__(self, grafo, prim_func, kruskal_func):
        self.grafo = grafo
        self.prim = prim_func
        self.kruskal = kruskal_func

        self.ventana = tk.Tk()
        self.ventana.title("Algoritmos: Prim, Kruskal y Dijkstra con Grafo Visual")
        self.ventana.geometry("600x500")

        # Variable del nodo origen
        self.origen_var = tk.StringVar(value=list(grafo.keys())[0])

        ttk.Label(self.ventana, text="Nodo Origen:").pack()
        ttk.OptionMenu(self.ventana, self.origen_var, list(grafo.keys())[0], *grafo.keys()).pack(pady=5)

        ttk.Button(self.ventana, text="Ejecutar Prim", command=self.mostrar_prim).pack(pady=5)
        ttk.Button(self.ventana, text="Ejecutar Kruskal", command=self.mostrar_kruskal).pack(pady=5)
        self.salida = tk.Text(self.ventana, height=15, width=70)
        self.salida.pack(pady=10)

    # =============================
    # DIBUJAR GRAFO Y RESULTADOS
    # =============================
    def dibujar_grafo(self, mst_edges=None, camino=None):
        G = nx.Graph()

        # añadir nodos y aristas
        for u in self.grafo:
            for v, peso in self.grafo[u]:
                G.add_edge(u, v, weight=peso)

        pos = nx.spring_layout(G, seed=42)

        # grafo base
        nx.draw(G, pos, with_labels=True, node_color="lightgray",
                edge_color="gray", node_size=800, font_size=10)

        # pesos
        etiquetas = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas)

        # mst en verde
        if mst_edges:
            nx.draw_networkx_edges(
                G, pos,
                edgelist=[(u, v) for u, v, _ in mst_edges],
                width=3,
                edge_color="green"
            )

        plt.show()

    # =============================
    # MOSTRAR PRIM
    # =============================
    def mostrar_prim(self):
        mst, total = self.prim(inicio = self.origen_var.get(), grafo = self.grafo)

        self.salida.delete("1.0", tk.END)
        self.salida.insert(tk.END, "=== PRIM ===\n")
        for u, v, p in mst:
            self.salida.insert(tk.END, f"{u} - {v} ({p})\n")
        self.salida.insert(tk.END, f"\nPeso total: {total}")

        self.dibujar_grafo(mst_edges=mst)

    # =============================
    # MOSTRAR KRUSKAL
    # =============================
    def mostrar_kruskal(self):
        mst, total = self.kruskal(self.grafo)

        self.salida.delete("1.0", tk.END)
        self.salida.insert(tk.END, "=== KRUSKAL ===\n")
        for u, v, p in mst:
            self.salida.insert(tk.END, f"{u} - {v} ({p})\n")
        self.salida.insert(tk.END, f"\nPeso total: {total}")

        self.dibujar_grafo(mst_edges=mst)

    # =============================
    # INICIAR GUI
    # =============================
    def iniciar(self):
        self.ventana.mainloop()
