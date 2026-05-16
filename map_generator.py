from map import Map
import random
from cell import Cell


class MapGenerator():
    map: Map


    def __init__(self, map: Map):
        self.map = map
        

    def generate(self):
        stack = []
        self.map.gen_map()
        self.map.print_map()
        entry_cell = self.map.table[self.map.entry_y][self.map.entry_x]
        entry_cell.visit()
        current_cell = entry_cell
        while True:
            neighbors = self.map.get_neighbors(current_cell)
            neighbors = self.map.get_unvisited_neighbors(neighbors)
            if len(neighbors) == 0:
                if stack:
                    current_cell = stack.pop()
                else:
                    break
            else:
                next_cell, direction = random.choice(neighbors)
                self.map.connect(current_cell, next_cell, direction)
                next_cell.visit()
                stack.append(current_cell)
                current_cell = next_cell
                print(next_cell, direction)

