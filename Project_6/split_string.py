""" Split string """
# Option a: split when we have seen half the total number of Hs in odd positions:
def split_S_odds(S: str):
    odd_S = sum(1 for i in range(1, len(S)+1) if S[i-1] == 'h' and i % 2 == 1)
    odd_counter = 0   # Keep count of the number of Hs in ODD positions we see.
    p_odds = None     # Index in S for which we have seen half the number of Hs in ODD positions.

    for i, aa in enumerate(S, start = 1):
        if aa == 'h':
            if i % 2 == 1:
                odd_counter += 1
                if p_odds is None and odd_counter == odd_S // 2:
                    p_odds = i
    
    return S[:p_odds], S[p_odds:]

# Option b: split when we have seen half the total number of Hs in even positions:
def split_S_evens(S: str):
    even_S = sum(1 for i in range(1, len(S)+1) if S[i-1] == 'h' and i % 2 == 0)  # Number of Hs in EVEN positions
    even_counter = 0  # Keep count of the number of Hs in EVEN positions we see.
    p_evens = None    # Index in the string for which we have seen half the number of Hs in EVEN positions.

    for i, aa in enumerate(S, start = 1):
        if aa == 'h':
            if i % 2 == 0:
                even_counter += 1
                if p_evens is None and even_counter == even_S // 2:
                    p_evens = i
    
    return S[:p_evens], S[p_evens:]