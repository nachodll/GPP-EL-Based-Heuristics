import GPP

def main():

    instances = ['G124.02', 'G124.16',
                 'G250.01', 'G250.02', 
                 'G250.04', 'G250.08',
                 'G500.01', 'U500.05',
                 'G1000.01', 'U1000.05']
    ks = [2, 3, 4]
    algorithms = ['BF', 'G', 
                  'EBF', 'EG', 
                  'ES', 'EPNES']
    reps = 10

    for instance in instances:
        filename = 'Johnson/' + instance
        for k in ks:
            gpp = GPP.GPP(filename, k)
            for algo in algorithms:
                for _ in range(reps):
                    gpp.solve(algo)

    return


if __name__ == "__main__":
    main()