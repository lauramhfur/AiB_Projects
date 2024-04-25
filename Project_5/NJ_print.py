from correct_DM import *

def NJ_print(S: list, DM: dict):

    T = []

    while len(S) > 3:

        def cluster(S, DM):
            nonlocal T

            print('\033[1m\033[96mInitialization\033[0m')
            print('\033[1mNo. taxa:\033[0m         ', len(S))
            print('\033[1mTaxa:\033[0m             ', S)
            print('\033[1mDM:\033[0m               ', DM)

            """ Step 1: a) Correcting DM b) Choosing pair to cluster """
            N = compute_N(S, DM)

            print('\33[1mCorrected DM:\33[0m     ', N)

            min_distances = {i: min((distance, idx) for idx, distance in enumerate(row) if distance != 0.0) for i, row in N.items()}  # Finding the shortest distance and its index for each sequence in N.
            S1 = min(min_distances, key = lambda k: min_distances[k][0])                                                              # Key with the minimum value among all minimum distances.
            S1_idx = next((i for i, seq in enumerate(DM) if seq == S1))
            S2_idx = min_distances[S1][1]                                                                                             # Extract the index of the second sequence. 
            S2 = S[S2_idx]                                                                                                            # Get name for the second sequence from S.

            k = [S1, S2]

            print('\33[1mPair to cluster:\33[0m  ', k, '\n')

            """ Step 2: Adding new node, k, to T """
            k_copy = k.copy()  # Create a copy of k to avoid overwriting.
            T.append(k_copy)   # Append the copy to T

            """ Step 3: Calculating distances to new cluster and adding edges, (k, i) and (k, j) """

            print('\033[1m\033[95mClustering\033[0m')

            # Adding edges:
            dij = {seq_i: DM[seq_i] for seq_i in DM.keys()}
            ri = {seq_i: round((1 / (len(DM) - 2)) * np.sum(DM_i), 2) for i, (seq_i, DM_i) in enumerate(DM.items()) for j in range(len(DM_i)) if i != j}
            
            diu = round(0.5 * dij[S1][S2_idx] + 0.5 * (ri[S1] - ri[S2]), 2)      # Distance from S1 to common node in cluster.
            dju = round(dij[S1][S2_idx] - diu, 2)                                # Distance from S2 to common node in cluster.

            cluster_idx = T.index(k)
            T[cluster_idx].append(diu)
            T[cluster_idx].append(dju)

            print(f'\33[1mDistance to node:\33[0m  {S1}: {diu}   {S2}: {dju}')

            # Calculating distances from other sequences to the new cluster:
            dijk = {}
            for i, seq_i in enumerate(DM.keys()):
                if seq_i not in (S1, S2):
                    dik = DM[S1][i]
                    djk = DM[S2][i]
                    dij = DM[S1][S2_idx]
                    dijk[seq_i] = round(0.5 * (dik + djk - dij), 2)
                dijk[(S1, S2)] = 0                                               # Converting cluster list to tuple, as lists are not allowed as keys.

            print('\033[1mDistance to k:\33[0m    ', dijk)

            """ Step 4: Update distance matrix """
            UDM = DM.copy()                                                      # Creating temporary distance matrix.
            UDM[(S1, S2)] = UDM.pop(S1)                                          # Overwrite key for first sequence. Note that this puts the (S1, S2) key in the last position of the dictionary.

            print('\033[1mOverwrite S1:\033[0m     ', UDM)

            del UDM[S2]                                                          # Delete key for the second sequence.

            for seq, dists in UDM.items():
                UDM[seq] = np.delete(dists, list(DM.keys()).index(S2))           # Delete column for the second sequence.
            
            print('\033[1mDelete S2:\33[0m        ', UDM)

            DM_idxs = {seq_i: i for i, seq_i in enumerate(DM.keys())}            # Sequence indexes in the input distance matrix.

            for i, seq_i in enumerate(UDM.keys()):
                if seq_i != (S1, S2):
                    for j, seq_j in enumerate(UDM.keys()):
                        if seq_j != seq_i:
                            if seq_j == (S1, S2):
                                UDM[seq_i][j] = dijk[seq_i]                      # Distance to k.
                            if seq_j != (S1, S2):
                                UDM[seq_i][j] = DM[seq_i][DM_idxs[seq_j]]        # Distance to other sequence.
                        if seq_j == seq_i:
                            UDM[seq_i][j] = 0                                    # Distance to self - always 0.
                if seq_i == (S1, S2):
                    for j, seq_j in enumerate(UDM.keys()):
                        UDM[seq_i][j] = dijk[seq_j]                              # Distances from k.
                            
            print('\033[1mUpdated DM:\33[0m       ', UDM, '\n')
            
            """ Step 5: Delete i and j from S and add the new taxon, k, to S. """
            
            S.remove(S1)
            S.remove(S2)
            S.append((S1, S2))

            return S, UDM, k

        S, DM, k = cluster(S, DM)  # k is the last cluster formed.

    """ Termination """
    i, j, m = S

    # Ensure m is k, otherwise swap the variable that is k for m.
    if m != tuple(k):
        if i == tuple(k):
            i, m = m, i
        elif j == k:
            j, m = m, j

    idx_i = list(DM.keys()).index(i)
    idx_j = list(DM.keys()).index(j)
    idx_m = list(DM.keys()).index(m)

    gamma_vi = round((DM[i][idx_j] + DM[i][idx_m] - DM[j][idx_m])/2, 3)
    gamma_vj = round((DM[j][idx_i] + DM[j][idx_m] - DM[i][idx_m])/2, 3)
    gamma_vm = round((DM[m][idx_i] + DM[m][idx_j] - DM[i][idx_j])/2, 3)

    T.append([i, gamma_vi])
    T.append([j, gamma_vj])
    T.append([m, gamma_vm])

    return T