import GPP

def main():

    algorithms = [
        'BF', 'G', 
        'EBF', 'EG', 
        'ES', 'EPNES'
    ]
    ks = [2, 3, 4]
    reps = 10
    ps = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64]
    ns = [124, 250]

    for n in ns:
        for p in ps:
            for i in range(1,4):
                filename = 'instances/' + str(n) + '.' + str(p).split('.')[-1] + '-' + str(i)
                for k in ks:
                    gpp = GPP.GPP(filename, k)
                    for algo in algorithms:
                        for _ in range(reps):
                            gpp.solve(algo)

    return


if __name__ == "__main__":
    main()