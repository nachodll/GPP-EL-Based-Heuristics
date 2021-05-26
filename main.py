import GPP

def main():

    instances = [
        'G500.02','G500.04'
    ]
    algorithms = [
        'BF', 'G', 
        'EBF', 'EG', 
        'ES', 'EPNES'
    ]
    ks = [2, 3, 4]
    reps = 10

    for i in range(50):
        filename = 'Johnson/' + 'G48.5-' + str(i)
        for k in ks:
            gpp = GPP.GPP(filename, k)
            for algo in algorithms:
                for _ in range(reps):
                    gpp.solve(algo)

    return


if __name__ == "__main__":
    main()