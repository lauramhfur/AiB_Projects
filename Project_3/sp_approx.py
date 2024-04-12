#############################
##  Functions and modules  ##
#############################

from read_fasta import read_fasta
from nw import nw
from extend_msa import msa
from typing import Sequence
import itertools

##################
##  Parameters  ##
##################

substMatrix = {
    'A': {'A': 0, 'C': 5, 'G': 2, 'T': 5, '-': 5, 'N': 5, 'R': 5, 'S': 5},
    'C': {'A': 5, 'C': 0, 'G': 5, 'T': 2, '-': 5, 'N': 5, 'R': 5, 'S': 5},
    'G': {'A': 2, 'C': 5, 'G': 0, 'T': 5, '-': 5, 'N': 5, 'R': 5, 'S': 5},
    'T': {'A': 5, 'C': 2, 'G': 5, 'T': 0, '-': 5, 'N': 5, 'R': 5, 'S': 5},
    '-': {'A': 5, 'C': 5, 'G': 5, 'T': 5, '-': 0, 'N': 5, 'R': 5, 'S': 5},
    'N': {'A': 5, 'C': 5, 'G': 5, 'T': 5, '-': 5, 'N': 5, 'R': 5, 'S': 5},
    'R': {'A': 5, 'C': 5, 'G': 5, 'T': 5, '-': 5, 'N': 5, 'R': 5, 'S': 5},
    'S': {'A': 5, 'C': 5, 'G': 5, 'T': 5, '-': 5, 'N': 5, 'R': 5, 'S': 5}
}

gapCost = 5

######################
##  Implementation  ##
######################

def sp_approx(sequences: Sequence, subst_matrix: dict, gap_cost: int) -> list[list]:

    """ Part 1: Initializing the MSA """

    seq_names = list(sequences.keys())
    alignments = {}

    """ a) Finding center sequence from distance matrix and average distances """

    # Distance matrix
    distanceMatrix = [[0] * len(seq_names) for _ in range(len(seq_names))]

    for i, seq_i in enumerate(seq_names):
        for j, seq_j in enumerate(seq_names):
            seqA = sequences[seq_i]
            seqB = sequences[seq_j]

            alignment = nw(seqA, seqB, subst_matrix, gap_cost)
            distanceMatrix[i][j] = alignment[2] # the distance is in the 2nd position in the ouput from NW()

            # Saving the full output from NW() for later
            if seq_i != seq_j and i < j:
                alignments[(seq_i, seq_j)] = alignment

    # Average distance from sequences to all other sequences
    avgDist = {}

    for i, seq_name in enumerate(seq_names):
        avg_distance = sum(distanceMatrix[i]) / len(distanceMatrix[i])
        avgDist[seq_name] = round(avg_distance, 2)

    ## Getting the center sequence - i.e., the sequence that is, on average, most similar to all other sequences
    centerSeq_name = min(avgDist, key = avgDist.get)

    """ b) Initializing alignment with the most similar sequences, with the center sequence in the first row """

    # Finding the first pair of sequences in the alignment - i.e., the sequences that are most similar
    firstPair_name = min(alignments, key = lambda k: alignments[k][2])

    M = []

    if firstPair_name[0] == centerSeq_name: # Case: the center sequence is the FIRST sequence in the pair-tuple
        M.append(alignments[firstPair_name][0])
        M.append(alignments[firstPair_name][1])

    else: # Case: the center sequence is the SECOND sequence in the pair-tuple
        M.append(alignments[firstPair_name][1])
        M.append(alignments[firstPair_name][0])

    M = list(map(list, zip(*M))) # creating list of columns

    """ Part 2: Computing the multiple sequence alignment using the 2-approximation algorithm, given in the extend_msa.py file """

    # Progressive MSA
    MA = []

    for i in alignments:
        A = []
        if i != firstPair_name and centerSeq_name in i: # Only looking at pairs that are not the first pair (which we already have) and sequences aligned with the center sequence
            if i[0] == centerSeq_name: # Case: the center sequence is the FIRST sequence in the pair-tuple
                A.append(alignments[i][0])
                A.append(alignments[i][1])
            
            else: # Case: the center sequence is the SECOND sequence in the pair-tuple
                A.append(alignments[i][1])
                A.append(alignments[i][0])

            A = list(map(list, zip(*A))) # creating list of columns
            MA = msa(M, A)

    MSA = ([''.join(column) for column in zip(*MA)])

    """ Part 3: Getting the SP score from the sum of columns """

    SP_score = []

    for i in MA:
        combs = list(itertools.combinations(i, 2))
        for pair in combs:
            score = subst_matrix[pair[0]][pair[1]]
            SP_score.append(score)

    return MSA, sum(SP_score)

############################################

sequences = read_fasta('brca1-full-6.fasta')
print(sp_approx(sequences, substMatrix, gapCost))