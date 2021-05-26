import GPP

def main():

    instances = [
        'G124.01', 'G124.04','G124.08', 
        'G124.32','G124.64','G250.16', 
        'G250.32', 'G250.64'
    ]
    algorithms = [
        'BF', 'G', 
        'EBF', 'EG', 
        'ES', 'EPNES'
    ]
    ks = [2, 3, 4]
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