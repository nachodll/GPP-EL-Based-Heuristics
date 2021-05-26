import GPP

def main():

    instances = [
        'G62.08','G62.16',
        'G62.32', 'G62.64'
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