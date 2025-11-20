def lcs_recursivo(X, Y, m, n):
    if m == 0 or n == 0:
        return 0
    if X[m - 1] == Y[n - 1]:
        return 1 + lcs_recursivo(X, Y, m - 1, n - 1)
    else:
        return max(lcs_recursivo(X, Y, m, n - 1), lcs_recursivo(X, Y, m - 1, n))


def lcs_dinamico_tabla(X, Y):
    m, n = len(X), len(Y)
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    return L, L[m][n]


def reconstruir_lcs(L, X, Y):
    i, j = len(X), len(Y)
    lcs = []
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs.append(X[i - 1])
            i -= 1
            j -= 1
        elif L[i - 1][j] >= L[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(lcs))