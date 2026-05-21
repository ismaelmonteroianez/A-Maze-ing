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
        self.reset_visited()

    def reset_visited(self):
        for row in self.map.table:
            for cell in row:
                cell.unvisit()

    def find_exit(self):
        entry_cell = self.map.table[self.map.entry_y][self.map.entry_x]
        exit_cell = self.map.table[self.map.exit_y][self.map.exit_x]
        queue = [entry_cell]
        entry_cell.visit()
        while queue:
            current_cell = queue.pop(0)
            if current_cell is exit_cell:
                break
            neighbors = self.map.get_neighbors(current_cell)
            neighbors = self.map.get_unwalled_neighbors(current_cell, neighbors)
            for neighbor in neighbors:
                if neighbor.visited is False:
                    neighbor.visit()
                    neighbor.father = current_cell
                    queue.append(neighbor)
        path_cell = exit_cell
        shortest_path: list[Cell] = []
        while path_cell is not entry_cell:
            shortest_path.append(path_cell)
            path_cell = path_cell.father
        shortest_path.append(path_cell)
        shortest_path.reverse()
        direction_list: list[str] = []
        for i in range(len(shortest_path) - 1):
            if shortest_path[i].y + 1 == shortest_path[i + 1].y:
                direction_list.append("S")
            if shortest_path[i].y - 1 == shortest_path[i + 1].y:
                direction_list.append("N")
            if shortest_path[i].x + 1 == shortest_path[i + 1].x:
                direction_list.append("E")
            if shortest_path[i].x - 1 == shortest_path[i + 1].x:
                direction_list.append("W")
        self.reset_visited()
        for cell in shortest_path:
            cell.visit()
