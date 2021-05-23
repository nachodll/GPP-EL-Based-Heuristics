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
        self.num_evals = 0
        self.num_steps = 0
        self.print_rate = 1
        self.verbose = True

        # set max_evals relative to n
        if self.n <= 500:
            self.max_evals = 10*(self.n**2)
        else:
            self.max_evals = 10 ** 6

        # remove first line from G (is redundant with n and num_edges)
        self.G.pop(0)

        # if k is not a factor of n, add empty nodes until it is
        if self.n%self.k !=0:
            num_empty_nodes = self.k - (self.n % self.k)
            self.n = self.n + num_empty_nodes
            for i in range(num_empty_nodes):
                self.G.append([])




    def read_graph(self):
        """Reads a graph in the Chaco input format from a file and 
        returns the same format as a list of lists"""

        with open(self.filename,'r') as file:
            G = []
            for line in file:
                l = []    
                for number in line.split():
                    # nodes are numbered from 1 to n
                    # substract 1 to get a 0 to n-1 range
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


    def avg_f_neighborhood (self, x):
        """Average objective function value of N(x)"""

        fx = self.f(x)
        c = 2 * (self.n - 1)
        d =((self.k - 1) * self.n**2) / (2*self.k)
        avg = fx + (c/d) * (self.avg_f() - fx)
        return avg


    def avg_f_partial_neighborhood(self, x):
        """Average objective function value of N_p(x)"""

        vnc = self.vertices_no_cut(x)
        fx = self.f(x)
        
        # Count the edges in the cut with 0 weigth
        cut_empty_edges = 0
        for i in range(self.k):
            for j in range(i+1, self.k):
                cut_empty_edges += len(vnc[i]) * len(vnc[j])
        d = ((self.k-1) * self.n**2) / (2 * self.k)  
        d_p = d - cut_empty_edges
        
        # Count the number of weights not contributing to
        # the new neighborhood (iterate pair by pair of blocks)
        W_p = 0
        for block1 in range(self.k):
            for block2 in range(block1+1, self.k):
                edges_to_vnc_1 = 0
                for i in range(self.n):
                    for v in vnc[block1]:
                        if i in self.G[v]:
                            edges_to_vnc_1 += 1
                W_p += edges_to_vnc_1 * len(vnc[block2])
                
                edges_to_vnc_2 = 0
                for i in range(self.n):
                    for v in vnc[block2]:
                        if i in self.G[v]:
                            edges_to_vnc_2 += 1
                W_p += edges_to_vnc_2 * len(vnc[block1])
        
        # Wave equation
        c = 2*self.n - 2
        b = 2*(self.n-(self.n/self.k))
        avg_partial_neighborhood = fx - (c/d_p)*fx + (b*self.num_edges - W_p) / d_p
    
        return avg_partial_neighborhood


    def random_partition (self):
        """Returns a list with n integers in
        range (0, k-1) in random order""" 

        x = []
        for i in range(self.k):
            x += [i]*int(self.n/self.k)
        random.shuffle(x)
        return x


    def vertices_no_cut (self, x):
        """Returns the vertices in each block which
        are not connected to any edge in the cut"""
        
        vnc = []
        for block in range(self.k):
            vnc.append([])
            for i in [i for i in range(self.n) if x[i]==block]:
                no_edge_in_cut = True
                for block2 in range(self.k):
                    if block != block2:
                        for j in [j for j in range(self.n) if x[j]==block2]:
                            if j in self.G[i]:
                                    no_edge_in_cut = False
                if no_edge_in_cut:
                    vnc[block].append(i)
            
        return vnc


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


    def first_neighborhood_improvement (self, x):
        """Returns the first solution having a better neighborhood
        average thant f(x) and [] if there is none"""
        
        current_avg= self.avg_f_neighborhood(x)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if x[i] != x[j]:
                    if self.num_evals >= self.max_evals:
                        break
                    y = x.copy()
                    y[i], y[j] = y[j], y[i]
                    if self.avg_f_neighborhood(y) < current_avg:
                        return y
        return []


    def best_neighborhood_improvement (self, x):
        """Returns the solution with the best neighborhood
        average in N(x) and [] if there is none"""

        best = []
        best_avg = self.avg_f_neighborhood(x)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if x[i] != x[j]:
                    if self.num_evals >= self.max_evals:
                        break
                    y = x.copy()
                    y[i], y[j] = y[j], y[i]
                    avg_fz = self.avg_f_neighborhood(y)
                    if avg_fz < best_avg:
                        best = y
                        best_avg = avg_fz
        return best


    def first_partial_neighborhood_improvement (self, x):
        """Returns the first solution with a better partial
        neighborhood average than x and [] uf there is none"""

        current_avg= self.avg_f_partial_neighborhood(x)
        vnc = self.vertices_no_cut(x)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if x[i] != x[j]:
                     # if they are in the partial neighborhood
                    if all(i not in l for l in vnc) or all(j not in l for l in vnc):
                        if self.num_evals >= self.max_evals:
                            break
                        y = x.copy()
                        y[i], y[j] = y[j], y[i]
                        if self.avg_f_partial_neighborhood(y) < current_avg:
                            return y
        return []
        

    def best_partial_neighborhood_improvement (self, x):
        """Returns the solution with the best partial neighborhood
        average in N_p(x) and [] if there is none"""

        best = []
        best_avg = self.avg_f_partial_neighborhood(x)
        vnc = self.vertices_no_cut(x)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if x[i] != x[j]:
                    # if they are in the partial neighborhood
                    if all(i not in l for l in vnc) or all(j not in l for l in vnc):
                        if self.num_evals >= self.max_evals:
                            break
                        y = x.copy()
                        y[i], y[j] = y[j], y[i]
                        avg_fz = self.avg_f_partial_neighborhood(y)
                        if avg_fz < best_avg:
                            best = y
                            best_avg = avg_fz
        return best


    def solve (self, algorithm):
        """Use a specified algorithm to find a
        solution for the gpp instance"""

        start_time = time.time()

        # Start with a random initial solution
        x = self.random_partition()

        # Keep moving until there is no improving neighbor
        while True:
            if algorithm == 'BF':
                # BEST FIRST seearch
                y = self.first_improvement(x)
            elif algorithm == 'G':
                # GREEDY  search
                y = self.best_improvement(x)
            elif algorithm == 'EBF':
                # ELEMENTARY BEST FIRST search
                y = self.first_neighborhood_improvement(x)
            elif algorithm == 'EG':
                # ELEMENTARY GREEDY search
                y = self.best_neighborhood_improvement(x)
            elif algorithm == 'PNEBF':
                # PARTIAL NEIGHBORHOOD ELEMENTARY BEST FIRST search
                y = self.first_partial_neighborhood_improvement(x)
            elif algorithm == 'PNG':
                # PARTIAL NEIGHBORHOOD ELEMENTARY BEST FIRST search
                y = self.best_partial_neighborhood_improvement(x)
            if not y:
                break
            x = y

            # Print info
            self.num_steps += 1
            if (self.verbose):
                if self.num_steps%self.print_rate==0:
                    print('Step ' + str(self.num_steps))
                    print('   f: ' + str(self.f(x)))
                    print('   Evaluations: ' + str(self.num_evals))

        # Check if it halted but it was not a local optima
        if (self.num_steps < self.max_evals):
            y = self.first_improvement(x)
            if y:
                print('TEN CUIDAOOOOO')
                print('Te has parao en '+ str(self.f(x)))
                print('Pero había un vecino con ' + str(self.f(y)))

        # Write results into file
        used_time = time.time() - start_time
        graph_name = self.filename.split('/')[-1]
        with open('results.csv', 'a', newline='') as results:
            writer = csv.writer(results, delimiter = '\t')
            writer.writerow([
                graph_name, self.k, algorithm, self.num_evals, 
                self.f(x), used_time, self.num_steps])

        # Reset counters
        self.num_evals = 0
        self.num_steps = 0

        return x