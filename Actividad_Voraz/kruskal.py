class UnionFind:
    def __init__(self, elementos):
        self.padre = {e: e for e in elementos}
        self.rango = {e: 0 for e in elementos}

    def find(self, x):
        if self.padre[x] != x:
            self.padre[x] = self.find(self.padre[x])
        return self.padre[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)

        if rx != ry:
            if self.rango[rx] < self.rango[ry]:
                self.padre[rx] = ry
            elif self.rango[rx] > self.rango[ry]:
                self.padre[ry] = rx
            else:
                self.padre[ry] = rx
                self.rango[rx] += 1
            return True
        return False


def kruskal(grafo):
    edges = []
    for u in grafo:
        for v, peso in grafo[u]:
            if (v, u, peso) not in edges:
                edges.append((u, v, peso))

    edges.sort(key=lambda x: x[2])   # ordenar por peso

    uf = UnionFind(grafo.keys())
    mst = []
    total = 0

    for u, v, p in edges:
        if uf.union(u, v):
            mst.append((u, v, p))
            total += p

    return mst, total


