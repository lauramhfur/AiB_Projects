""" Find possible match positions """
# Option a: look for odds in S1 and evens in S2:
def find_contacts_odd(S1: str, S2: str):
    
    S_indices = list(range(1, len(S1)+len(S2)+1))
    S1_indices = list(range(1, len(S1)+1))
    S2_indices = list(range(len(S1)+1, len(S_indices)+1))
    
    odd_pos_S1 = []
    even_pos_S2 = []
    for i in range(1, len(S1)+1):
        if S1[i-1] == 'h' and i % 2 == 1:
            odd_pos_S1.append(S1_indices[i-1])
    
    for j in range(len(S2), 0, -1):
        if S2[j-1] == 'h' and S2_indices[j-1] % 2 == 0:
            even_pos_S2.append(S2_indices[j-1])

    matches = None
    matched_positions = None

    if len(odd_pos_S1) == len(even_pos_S2):
        matches = len(odd_pos_S1)
        matched_positions = dict(zip(odd_pos_S1, even_pos_S2))
    
    if len(odd_pos_S1) < len(even_pos_S2):
        difference = len(even_pos_S2) - len(odd_pos_S1)
        matches = len(even_pos_S2) - difference
        even_pos_S2 = even_pos_S2[:-difference]
        matched_positions = dict(zip(odd_pos_S1, even_pos_S2))

    if len(odd_pos_S1) > len(even_pos_S2):
        difference = len(odd_pos_S1) - len(even_pos_S2)
        matches = len(odd_pos_S1) - difference
        odd_pos_S1 = odd_pos_S1[:-difference]
        matched_positions = dict(zip(odd_pos_S1, even_pos_S2))

    return matches, matched_positions

# Option b: look for evens in S1 and odds in S2:
def find_contacts_even(S1: str, S2: str):

    S_indices = list(range(1, len(S1)+len(S2)+1))
    S1_indices = list(range(1, len(S1)+1))
    S2_indices = list(range(len(S1)+1, len(S_indices)+1))

    # If we look at evens in from left to right in S1 and odds in S2 from right to left:
    even_pos_S1 = []
    odd_pos_S2 = []

    for i in range(1, len(S1)+1):
        if S1[i-1] == 'h' and i % 2 == 0:
            even_pos_S1.append(S1_indices[i-1])
    
    for j in range(len(S2), 0, -1):
        if S2[j-1] == 'h' and S2_indices[j-1] % 2 == 1:
            odd_pos_S2.append(S2_indices[j-1])

    matches = None
    matched_positions = None

    if len(even_pos_S1) == len(odd_pos_S2):
        matches = len(even_pos_S1)
        matched_positions = dict(zip(even_pos_S1, odd_pos_S2))
    
    elif len(even_pos_S1) < len(odd_pos_S2):
        difference = len(odd_pos_S2) - len(even_pos_S1)
        matches = len(odd_pos_S2) - difference
        odd_pos_S2 = odd_pos_S2[:-difference]
        matched_positions = dict(zip(even_pos_S1, odd_pos_S2))

    elif len(even_pos_S1) > len(odd_pos_S2):
        difference = len(even_pos_S1) - len(odd_pos_S2)
        matches = len(even_pos_S1) - difference
        even_pos_S1 = even_pos_S1[:-difference]
        matched_positions = dict(zip(even_pos_S1, odd_pos_S2))
            
    return matches, matched_positions