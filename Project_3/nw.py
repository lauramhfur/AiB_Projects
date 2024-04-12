from typing import Sequence

def nw(seq1: Sequence, seq2: Sequence, subst_matrix: dict, gap_cost: int) -> object:
    
    # Initialize the scoring matrix
    n, m = len(seq1), len(seq2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Initialize the first row and column with gap penalties
    for i in range(1, n + 1):
        dp[i][0] = dp[i-1][0] + gap_cost
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j-1] + gap_cost

    # Fill in the rest of the matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match_score = dp[i-1][j-1] + subst_matrix[seq1[i-1]][seq2[j-1]]
            delete_score = dp[i-1][j] + gap_cost
            insert_score = dp[i][j-1] + gap_cost
            dp[i][j] = min(match_score, delete_score, insert_score)

    # Backtrack to find the alignment
    aligned_seq1, aligned_seq2 = '', ''
    i, j = n, m

    while i > 0 or j > 0:
        if i > 0 and dp[i][j] == dp[i-1][j] + gap_cost:
            aligned_seq1 = seq1[i-1] + aligned_seq1
            aligned_seq2 = "-" + aligned_seq2
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j-1] + gap_cost:
            aligned_seq1 = "-" + aligned_seq1
            aligned_seq2 = seq2[j-1] + aligned_seq2
            j -= 1
        else:
            aligned_seq1 = seq1[i-1] + aligned_seq1
            aligned_seq2 = seq2[j-1] + aligned_seq2
            i -= 1
            j -= 1
    return list(aligned_seq1), list(aligned_seq2), dp[n][m]