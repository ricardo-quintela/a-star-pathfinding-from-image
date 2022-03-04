import pygame
from settings import *
import math

class Node():
    def __init__(self, coords, start, end):
        self.start = start
        self.end = end

        x = coords[0]
        y = coords[1]

        #coords
        self.coords = coords
        # parent
        self.parent = 'NULL'
        #costs
        self.Gcost, self.Hcost, self.Fcost = self.calculate_costs(coords, start, end)
        #vizinhos
        self.neighbors = []


    def calculate_norm(self, a, b):
        #calculates the size of the vector
        return int(round(math.sqrt(sum([i**2 for i in [b[i] - k for i,k in enumerate(a)]])) * 10,0))

    def calculate_costs(self, coords, start_pos, end_pos):
        #calculates all distances to start and end cell (COSTS)
        Gcost = self.calculate_norm(coords, start_pos) // tilesize
        Hcost = self.calculate_norm(coords, end_pos) // tilesize
        Fcost = Gcost + Hcost
        return Gcost, Hcost, Fcost

    def calculate_neigbors(self, coords):
        #calculates all 4 cells around a given cell
        nodes = [[coords[0] + 30, coords[1]], [coords[0] - 30, coords[1]], [coords[0], coords[1] + 30], [coords[0], coords[1] - 30]]
        neighbors = []
        for node in nodes:
            if node[0] < 0 or node[1] < 0:
                continue
            new_node = Node(node, self.start, self.end)
            neighbors.append(new_node)
            print("Analizando ({}, {}), Gcost: {}, Hcost: {}, Fcost: {}".format(new_node.coords[0], new_node.coords[1], new_node.Gcost, new_node.Hcost, new_node.Fcost))
        return neighbors