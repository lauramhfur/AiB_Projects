import numpy as np

def init_score_matrix(file):
    raw = open(file, 'r').read()
    lines_sep = raw.split('\n')
    nested_dict = {}

    for line in lines_sep:
        parsed_line = line.split()
        key = parsed_line[0]
        scores_per_nucl = {}

        for char in range(1, len(parsed_line)):
            scores_per_nucl[lines_sep[char-1][0]] = int(parsed_line[char])
        
        nested_dict[key] = scores_per_nucl
    
    return nested_dict

def init_dist_matrix(phylip):
    distance_matrix = {}
    with open(phylip, 'r') as f:
        next(f)
        for line in f:
            line_element = line.split()
            seq_name = line_element.pop(0)
            converted_numbers = np.array(line_element, dtype = float)
            distance_matrix[seq_name] = converted_numbers
    return distance_matrix