import numpy as np
import copy

def compute_N(S, DM):
    N = copy.deepcopy(DM)

    dij = {seq_i: DM[seq_i] for seq_i in DM.keys()}
    ri = {seq_i: round((1/(len(S)-2)) * np.sum(distances_i), 2) for i, (seq_i, distances_i) in enumerate(DM.items()) for j in range(len(distances_i)) if i != j}
    
    for i, seq_i in enumerate(DM.keys()):
        for j, seq_j in enumerate(DM.keys()):
            if i != j:
                N[seq_i][j] = dij[seq_i][j] - (ri[seq_i] + ri[seq_j])
            else:
                N[seq_i][j] = 0
    return N