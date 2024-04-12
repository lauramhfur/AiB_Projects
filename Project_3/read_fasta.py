from Bio import SeqIO

def read_fasta(file_path):
    sequences = {}
    with open(file_path, 'r') as file:
        for record in SeqIO.parse(file, 'fasta'):
            sequences[record.id] = str(record.seq)
    return sequences