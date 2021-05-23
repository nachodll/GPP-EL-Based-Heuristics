import random
import csv
import time


class GPP:

    def __init__(self, filename, k):
        self.filename = filename
        self.G = self.read_graph()
        self.k = k
        self.n = self.G[0][0]+1
        self.num_edges = self.G[0][1]+1
        self.max_evals = 10*(self.n**2)
        self.num_evals = 0
        self.num_steps = 0
        self.algorithm = 'elementary_first'
        self.print_rate = 1

        # Remove first line from G
        self.G.pop(0)

        # If k is not a factor of n, add empty nodes until it is
        if self.n%self.k !=0:
            num_empty_nodes = self.k - (self.n % self.k)
            self.n = self.n + num_empty_nodes
            for i in range(num_empty_nodes):
                self.G.append([])

        # exception for max_evals
        if self.n > 500:
            self.max_evals = 10 ** 6




    def read_graph(self):
        """Reads a graph in the Chaco input format from a file and 
        returns the same format as a list of lists"""

        with open(self.filename,'r') as file:
            G = []
            for line in file:
                l = []    
                for number in line.split():
                    l.append(int(number)-1)
                G.append(l)
        return G


    def f (self, x):
        """Computes the objective function value 
        for incumbent solution x"""

        self.num_evals += 1
        f = 0
        for i in range (self.n):
            for j in self.G[i]:
                f += (1,0)[x[i]==x[j]]
        return f/2


    def avg_f (self):
        """Average objective function of the search space"""

        avg = (self.n*(self.k-1))/(self.k*(self.n-1)) * self.num_edges
        return avg


    def avg_fy (self, x):
        """Average objective function value of N(x)"""

        fx = self.f(x)
        c = 2 * (self.n - 1)
        d =((self.k - 1) * self.n**2) / (2*self.k)
        avg = fx + (c/d) * (self.avg_f() - fx)
        return avg


    def random_partition (self):
        """Returns a list with n integers in
        range (0, k-1) in random order""" 

        x = []
        for i in range(self.k):
            x += [i]*int(self.n/self.k)
        random.shuffle(x)
        return x

    
    def random_neighbor (self, x):
        """Returns a random exchange neighbor in N(x)""" 

        i = random.randint(0, len(x))
        j = random.randint(0, len(x))
        while x[i] == x[j]:
            j = random.randint(0, len(x))
        x[i], x[j] = x[j], x[i]
        return x


    def first_improvement (self, x):
        """Returns first solution in N(x) better than x
        and [] if there is none""" 
        
        fx = self.f(x)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if self.num_evals >= self.max_evals:
                    break
                if x[i] != x[j]:
                    y = x.copy()
                    y[i], y[j] = y[j], y[i]
                    if self.f(y) < fx:
                        return y
        return []


    def best_improvement (self, x):
        """Returns the best solution in N(x) if it is 
        better than x and [] if there is none""" 

        fx = self.f(x)
        best = []
        fbest = fx
        for i in range(self.n):
            for j in range(i+1, self.n):
                if x[i] != x[j]:
                    if self.num_evals >= self.max_evals:
                        break
                    y = x.copy()
                    y[i], y[j] = y[j], y[i]
                    fy =  self.f(y)
                    if fy < fx and fy < fbest:
                        best = y
                        fbest = fy
        return best


    def elementary_improvement (self, x):
        """Returns the best solution in N(x) if it is 
        better than x and [] if there is none"""

        best = []
        best_avg = self.avg_fy(x)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if x[i] != x[j]:
                    if self.num_evals >= self.max_evals:
                        break
                    y = x.copy()
                    y[i], y[j] = y[j], y[i]
                    avg_fz = self.avg_fy(y)
                    if avg_fz < best_avg:
                        best = y
                        best_avg = avg_fz
        return best


    def elementary_first (self, x):
        """Returns the best solution in N(x) if it is 
        better than x and [] if there is none""" 
        
        current_avg= self.avg_fy(x)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if x[i] != x[j]:
                    if self.num_evals >= self.max_evals:
                        break
                    y = x.copy()
                    y[i], y[j] = y[j], y[i]
                    if self.avg_fy(y) < current_avg:
                        return y
        return []


    def local_search (self):
        """Local search implementation to find a
        k-partition of graph G"""

        # Start with a random initial solution
        x = self.random_partition()

        # Keep moving until there is no improving neighbor
        while True:
            if self.algorithm == 'BF':
                y = self.first_improvement(x)
            elif self.algorithm == 'G':
                y = self.best_improvement(x)
            elif self.algorithm == 'EBF':
                y = self.elementary_first(x)
            elif self.algorithm == 'EG':
                y = self.elementary_improvement(x)
            if not y:
                break
            x = y

            # Print info
            self.num_steps += 1
            # if self.num_steps%self.print_rate==0:
            #     print('Step ' + str(self.num_steps))
            #     print('   f: ' + str(self.f(x)))
            #     print('   Evaluations: ' + str(self.num_evals))

        return x

    
    def solve (self, algorithm):

        start_time = time.time()
        
        self.algorithm = algorithm
        x = self.local_search()

        # Write results into file
        used_time = time.time() - start_time
        graph_name = self.filename.split('/')[-1]
        with open('results.csv', 'a', newline='') as results:
            writer = csv.writer(results, delimiter = '\t')
            writer.writerow([
                graph_name, self.k, self.algorithm, self.num_evals, 
                self.f(x), used_time, self.num_steps])

        # Reset counters
        self.num_evals = 0
        self.num_steps = 0

        return x