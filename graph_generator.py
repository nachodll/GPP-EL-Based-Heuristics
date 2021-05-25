import random

def random_johnson_graph (n, p):
    G = []
    for i in range(n+1):
        G.append([])
    G[0] = [n, 0]

    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if random.random() < p:
                G[0][1] += 1
                G[i].append(j)
                G[j].append(i)
    return G

def graph_to_file (G, filename):
    gstr = ''
    for line in G:
        for number in line:
            gstr += str(number) + ' '
        gstr += '\n'
    
    with open(filename, 'w') as f:
        f.write(gstr)
    return

# Create a random graph
n = 250
p = 0.64
G = random_johnson_graph(n, p)

# Save it
filename = 'Johnson/G' + str(n) + '.' + str(p).split('.')[-1]
graph_to_file(G, filename)