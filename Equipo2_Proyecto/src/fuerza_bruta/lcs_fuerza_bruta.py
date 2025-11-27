def lcs_brute_force(X, Y, m, n):
    if m == 0 or n == 0:
        return 0
    if X[m - 1] == Y[n - 1]:
        return 1 + lcs_brute_force(X, Y, m - 1, n - 1)
    else:
        return max(lcs_brute_force(X, Y, m, n - 1), lcs_brute_force(X, Y, m - 1, n))