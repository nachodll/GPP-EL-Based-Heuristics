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
    

    for p in [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64]:
        for i in range(3):
            filename = 'instances/G214.' + str(p).split('.')[-1] + '-' + str(i)
            for k in ks:
                gpp = GPP.GPP(filename, k)
                for algo in algorithms:
                    for _ in range(reps):
                        gpp.solve(algo)

    return


if __name__ == "__main__":
    main()