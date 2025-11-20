import heapq

def prim(grafo, inicio='A'):
    visitados = set([inicio])
    edges = []
    heap = []

    # agregar aristas iniciales
    for vecino, peso in grafo[inicio]:
        heapq.heappush(heap, (peso, inicio, vecino))

    mst = []
    total = 0

    while heap:
        peso, u, v = heapq.heappop(heap)
        if v not in visitados:
            visitados.add(v)
            mst.append((u, v, peso))
            total += peso

            # agregar aristas del nuevo nodo
            for vecino, peso2 in grafo[v]:
                if vecino not in visitados:
                    heapq.heappush(heap, (peso2, v, vecino))

    return mst, total


