#!/usr/bin/env python

from itertools import permutations
from math import ceil, sqrt
import matplotlib.pyplot as plt
from pprint import pprint


def get_squares(n):
    return {(k*k) for k in range(2, ceil(sqrt(2*n-1)))}

def getList(n):

    squares = get_squares(n)

    print(squares)
    return
    for permutation in permutations(range(1, n+1)):

        for a, b in zip(permutation, permutation[1:]):
            if a + b not in squares:
                break
        else:
            return permutation

    return False

        
def get_edges(n):
    squares = get_squares(n)
    edges = []

    for square in squares:
        start = max(square - n, 1)
        end = n + 1

        i = start
        while i < square - i:
            edges.append((i, square - i))
            i += 1

    return edges

def get_adjancency_list(n, edges):

    adj = {i: set() for i in range(1, n+1)}

    for v1, v2 in edges:
        adj[v1].add(v2)
        adj[v2].add(v1)

    return adj

def path_can_exist(adjacency_list):
    one_degree_verts = 0

    for adjacent_verts in adjacency_list.values():
        num_adjacent = len(adjacent_verts)

        if num_adjacent == 0:
            return False
        elif num_adjacent == 1:
            one_degree_verts += 1

    return one_degree_verts <= 2

def simplify(adj):
    count = 0
    
    nodes_to_ignore = set()

    for node in adj.keys():
        #print("node: ", node)

        if node in nodes_to_ignore:
            continue

        for neighbor in adj[node]:
            #print("  neighbor: ", neighbor)

            if neighbor == node or neighbor in nodes_to_ignore:
                continue

            for distant_neighbor in adj[neighbor]:

                if distant_neighbor == node or distant_neighbor in nodes_to_ignore:
                    continue

                #print("    distant: ", distant_neighbor)

                #print("      node adj to distant: ", node in adj[distant_neighbor])
                if node in adj[distant_neighbor]:
                    count += 1
                    nodes_to_ignore.add(node)
                    nodes_to_ignore.add(neighbor)
                    nodes_to_ignore.add(distant_neighbor)
                    break
            else:
                continue
            break


    print(count)


def create_adj_matrix(adj_list):
    size = range(len(adj_list))
    matrix = [[0 for _ in size] for _ in size]

    for node, neighbors in adj_list.items():
        for neighbor in neighbors:
            matrix[node-1][neighbor-1] = 1
            matrix[neighbor-1][node-1] = 1

    return matrix

class Graph(): 
    def __init__(self, vertices): 
        self.graph = [[0 for column in range(vertices)]for row in range(vertices)] 
        self.V = vertices 
  
    ''' Check if this vertex is an adjacent vertex  
        of the previously added vertex and is not  
        included in the path earlier '''
    def isSafe(self, v, pos, path): 
        # Check if current vertex and last vertex  
        # in path are adjacent 
        if self.graph[ path[pos-1] ][v] == 0: 
            return False
  
        # Check if current vertex not already in path 
        for vertex in path: 
            if vertex == v: 
                return False
  
        return True
  
    # A recursive utility function to solve  
    # hamiltonian cycle problem 
    def hamCycleUtil(self, path, pos): 
  
        # base case: if all vertices are  
        # included in the path 
        if pos == self.V: 
            # Last vertex must be adjacent to the  
            # first vertex in path to make a cyle 
            if self.graph[ path[pos-1] ][ path[0] ] == 1: 
                return True
            else: 
                return False
  
        # Try different vertices as a next candidate  
        # in Hamiltonian Cycle. We don't try for 0 as  
        # we included 0 as starting point in hamCycle() 
        for v in range(1,self.V): 
  
            if self.isSafe(v, pos, path) == True: 
  
                path[pos] = v 
  
                if self.hamCycleUtil(path, pos+1) == True: 
                    return True
  
                # Remove current vertex if it doesn't  
                # lead to a solution 
                path[pos] = -1
  
        return False
  
    def hamCycle(self): 
        path = [-1] * self.V 
  
        ''' Let us put vertex 0 as the first vertex  
            in the path. If there is a Hamiltonian Cycle,  
            then the path can be started from any point 
            of the cycle as the graph is undirected '''
        path[0] = 0
  
        if self.hamCycleUtil(path,1) == False: 
            print("Solution does not exist\n")
            return False
  
        self.printSolution(path) 
        return True
  
    def printSolution(self, path): 
        print("Solution Exists: Following is one Hamiltonian Cycle")
        sequence = []
        for vertex in path: 
            sequence.append(vertex+1)

        print(sequence)


n = 32
edges = get_edges(n)
adj = get_adjancency_list(n, edges)

matrix = create_adj_matrix(adj)

g = Graph(n)
g.graph = matrix
g.hamCycle()



simple = {
    1: {2, 3},
    2: {1, 3, 4},
    3: {1, 2, 4},
    4: {2, 3}
}


#simplify(adj)

draw = False
if draw:
    import networkx as nx
    g = nx.Graph()
    g.add_nodes_from(range(1,n+1))
    g.add_edges_from(edges)
    nx.draw(g)
    plt.show()

