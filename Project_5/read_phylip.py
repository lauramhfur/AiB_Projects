import numpy as np 

def initiate_DM(phylip):
    distance_matrix = {}
    with open(phylip, 'r') as f:
        next(f) # Skipping first line, which is the number of sequences.
        for line in f:
            line_element = line.split()
            seq_name = line_element[0].rstrip('_')
            converted_numbers = np.array(line_element[1:], dtype = float) # Numpy array for less space consumption
            distance_matrix[seq_name] = converted_numbers
    return distance_matrix