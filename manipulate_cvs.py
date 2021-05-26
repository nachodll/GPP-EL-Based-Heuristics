import csv
import statistics as stats

for k in [2, 3, 4]:
    with open('results/final_results.csv', 'r', newline='') as results:
        filename = 'results/mediansk' + str(k) + '.csv'
        with open(filename, 'w', newline='') as medians:
            reader = csv.DictReader(results, delimiter='\t')
            writer = csv.writer(medians, delimiter=',')

            # Writer headers
            writer.writerow(['instances', 'BF', 'G', 'EBF', 'EG', 'ES', 'EPNS'])

            values = []
            medians = []
            algo = ''
            num_lines = 0
            for line in reader:
                values.append(float(line['value']))
                # every 10 lines we change algorithm and compute median
                if num_lines%10 == 9:
                    algo = line['algorithm']
                    median = stats.median(values)
                    medians.append(median)
                    values = []

                # every 60 lines we change k and write a line
                if num_lines%60 == 59:
                    if k == float(line['k']):
                        writer.writerow([
                            line['instance'],
                            medians[0],
                            medians[1],
                            medians[2],
                            medians[3],
                            medians[4],
                            medians[5],
                        ])
                    medians = []

                num_lines += 1