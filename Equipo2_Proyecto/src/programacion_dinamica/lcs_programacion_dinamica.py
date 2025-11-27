def lcs_dinamyc_programing(tokens_a, tokens_b):
    m = len(tokens_a)
    n = len(tokens_b)
    
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if tokens_a[i-1] == tokens_b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    index = dp[m][n]
    lcs_tokens = [""] * (index + 1)
    lcs_tokens[index] = "" 

    i, j = m, n
    while i > 0 and j > 0:
        if tokens_a[i-1] == tokens_b[j-1]:
            lcs_tokens[index-1] = tokens_a[i-1]
            i -= 1
            j -= 1
            index -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
            
    return lcs_tokens[:-1]