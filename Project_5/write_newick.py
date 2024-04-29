def newick(nj_out):
    new = '('
    
    for cluster, subcluster in nj_out.items():

        if cluster != 'v':
            for seq in cluster:
                if type(seq) != tuple:
                    if seq != cluster[-1]:
                        new = new + f'{seq}:{subcluster[seq]},'
                    else:
                        new = new + f'{seq}:{subcluster[seq]})'

                if type(seq) == tuple:
                    new = new + '('
                    for element in seq:
                        if element != seq[-1]:
                                new = new + f"{element}:{subcluster[seq][element]},"
                        else:
                                new = new + f"{element}:{subcluster[seq][element]}):{subcluster['u']}"

        if cluster != list(nj_out.keys())[-1]:
            if cluster == list(nj_out.keys())[-2]:
                pass
            else:
                new = new + ',('

        if cluster == list(nj_out.keys())[-1]:
            new = new + f':{subcluster}'

    new = new + ');'

    return new