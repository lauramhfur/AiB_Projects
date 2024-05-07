def make_fold(S1_best: str, S2_best: str, match_positions: dict, best_of_oe_eo: str):

    S = S1_best + S2_best
    HP_directions = ''

    B_even = {key: next_key - key for key, next_key in zip(match_positions.keys(), list(match_positions.keys())[1:])}      # Distance from current even to next even match position.
    B_odd = {key: key - next_key for key, next_key in zip(match_positions.values(), list(match_positions.values())[1:])}  # Distance from current odd to next odd match position. 

    # General, simple approach
    i = 1
    while i < len(S1_best):
        if best_of_oe_eo == 'E-O':  # Sequence 1 focuses on Hs in the even positions.
            if i not in B_even:
                HP_directions = HP_directions + 'e'  # Move right

            if i in B_even:
                if B_even[i] % 2 == 1:                                 
                    move_up = B_even[i] // 2
                    move_right = 1
                    move_down = move_up
                    HP_directions = HP_directions + 'n' * move_up + 'e' + 's' * move_down

                    i += move_up + move_right + move_down # Increase i by the total number of movements made.

                if B_even[i] % 2 == 0:
                    move_up = B_even[i] // 2 - 1
                    move_right = 1
                    move_down = move_up
                    move_right = 1
                    HP_directions = HP_directions + 'n' * move_up + 'e' + 's' * move_down + 'e'

                    i += move_up + move_right + move_down + move_right

            i += 1
            continue

        if best_of_oe_eo == 'O-E':  # Sequence 1 focuses on Hs in the odd positions.
            if i not in B_odd:
                HP_directions = HP_directions + 'e'
            if i in B_odd:
                if B_odd[i] % 2 == 1:
                    move_up = B_odd[i] // 2
                    move_right = 1
                    move_down = move_up
                    HP_directions = HP_directions + 'n' * move_up + 'e' + 's' * move_down

                    i += move_up + move_right + move_down  

                if B_odd[i] % 2 == 0:
                    move_up = B_odd[i] // 2 - 1
                    move_right = 1
                    move_down = move_down
                    move_right = 1
                    HP_directions = HP_directions + 'n' * move_up + 'e' + 's' * move_down + 'e'

                    i += move_up + move_right + move_down + move_right
                
            i += 1
            continue
        print(i)
    HP_directions = HP_directions + 's'  # After finishing up with sequence 1, go one step down and get started on sequence 2.

    i = len(S1_best)+1
    while i < len(S):
        if best_of_oe_eo == 'E-O': # Sequence 2 focuses on Hs in the odd positions.
            if i not in B_odd:
                HP_directions = HP_directions + 'w'

            if i in B_odd:
                if B_odd[i] % 2 == 1:             
                    move_down = B_odd[i] // 2
                    move_left = 1
                    move_up =  move_down
                    move_left = 1
                    HP_directions = HP_directions + 's' * move_down + 'w' + 'n' * move_up + 'w'

                    i += move_down + move_left + move_up + move_left

                if B_odd[i] % 2 == 0:
                    move_down = B_odd[i] // 2 - 1
                    move_left = 1
                    move_up = move_down
                    move_left = 1
                    HP_directions = HP_directions + 's' * move_down + 'w' + 'n' * move_up + 'w'

                    i += move_down + move_left + move_up + move_left

            i += 1
            continue

        if best_of_oe_eo == 'O-E': # Sequence 2 focuses on Hs in the even positions.
            if i not in B_even:
                HP_directions = HP_directions + 'e'

            if i in B_even:
                if B_even[i] % 2 == 1:
                    move_down = B_even[i] // 2
                    move_left = 1
                    move_up = move_down
                    HP_directions = HP_directions + 's' * move_down + 'w' + 'n' * move_up

                    i += move_down + move_left + move_up

                if B_even[i] % 2 == 0:
                    move_down = B_even[i] // 2 - 1
                    move_left = 1
                    move_up = move_down
                    move_left = 1
                    HP_directions = HP_directions + 's' * move_down + 'w' + 'n' * move_up + 'w'

                    i += move_down + move_up + move_left

            i += 1
            continue

    return HP_directions