from split_string import *
from match_positions import *

""" Trying all combinations of 1) split type and 2) even or odd Hs on the respective strings - to find the best orientation when matching positions """
def best_combination(S: str):
    S1_odds_first = split_S_odds(S)[0]
    S2_odds_first = split_S_odds(S)[1]

    OddsFirst_EO = find_contacts_even(S1_odds_first, S2_odds_first)
    OddsFirst_OE = find_contacts_odd(S1_odds_first, S2_odds_first)

    S1_evens_first = split_S_evens(S)[0]
    S2_evens_first = split_S_evens(S)[1]

    EvensFirst_EO = find_contacts_even(S1_evens_first, S2_evens_first)
    EvensFirst_OE = find_contacts_odd(S1_evens_first, S2_evens_first)

    # Collecting everything in a matrix:
    matrix = {'Half of evens-split': {'O-E': EvensFirst_OE[0], 'E-O': EvensFirst_EO[0]}, 
            'Half of odds-split': {'O-E': OddsFirst_OE[0], 'E-O': OddsFirst_EO[0]}}
    
    # Finding the optimal combination:
    best_split_type = None
    best_of_oe_eo = None
    max_matches = float('-inf')

    for outer_key, inner_dict in matrix.items():
        for inner_key, value in inner_dict.items():
            if value > max_matches:
                best_split_type = outer_key
                best_of_oe_eo = inner_key
                max_matches = value

    if best_of_oe_eo == 'O-E':
        if best_split_type.endswith('odds-split'):
            matched_positions = OddsFirst_OE[1]
            best_split = S1_odds_first, S2_odds_first
        else:
            matched_positions = EvensFirst_OE[1]
            best_split = S1_evens_first, S2_evens_first
    if best_of_oe_eo == 'E-O':
        if best_split_type.endswith('evens_split'):
            matched_positions = EvensFirst_EO[1]
            best_split = S1_evens_first, S2_evens_first
        else:
            matched_positions = OddsFirst_EO[1]
            best_split = S1_odds_first, S2_odds_first

    """ Calculating the best possible free energy """
    scores = 0
    for pos_S1, pos_S2 in matched_positions.items():
        if pos_S1 == 1 and pos_S2 == len(S):
            possible_bonds = 2 * (3 - 1)        # 3 possible non-local H-H bonds can be formed at the ends, but since both ends match with each other, we subtract 1 from each.
            scores = scores + possible_bonds  
        
        if pos_S1 == 1 and pos_S2 < len(S):     # 3 possible non-local H-H bonds at the end, and 2 possible inside, but since they both match, we subtract 1 from each.
            possible_bonds = (3 - 1) + (2 - 1)
            scores = scores + possible_bonds

        if pos_S1 > 1 and pos_S2 == len(S):     # Same case as above.
            possible_bonds = (3 - 1) + (2 - 1)
            scores = scores + possible_bonds
        
        if pos_S1 > 1 and pos_S2 < len(S):      # 2 possible non-local H-H bonds can be formed inside the string, but since they both match, we subtract 1 from each.
            possible_bonds = 2 * (2 - 1)
            scores = scores + possible_bonds
                
    bestFree = -1 * scores                      # Multiplying by -1 because one match is a decrease in free energy.

    return best_split_type, best_of_oe_eo, best_split, matched_positions, bestFree