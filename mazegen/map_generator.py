from mazegen.map import Map
import random
from mazegen.cell import Cell
"""
Maze generation and solving engine.

This module implements the full maze generation pipeline, including:
- Recursive backtracking maze generation
- Optional "42" pattern blocking
- Non-perfect maze modification
- Shortest path computation
- Output file serialization in the required format
"""


class InvalidConfiguration(Exception):
    pass


class MapGenerator():
    """
    Main maze generation and solving controller.
    This class is responsible for generating a valid maze based on
    a configuration, applying optional constraints (such as the "42"
    pattern), modifying the maze for non-perfect mode, and computing
    the shortest path between entry and exit.
    """
    map: Map

    def __init__(self, config: dict[str, str]):
        """
        Initialize the maze generator.
        Creates an internal Map instance using the provided configuration.
        Args:
            config (dict[str, str]): Parsed configuration dictionary.
        Returns:
            None
        """
        self.map = Map(config)

    def block_42_cells(self) -> None:
        """
        Block cells to form the required "42" pattern in the maze.
        Marks a predefined pattern of cells as blocked relative to the
        center of the maze. Ensures entry and exit are not placed inside
        the blocked pattern.
        Raises:
            InvalidConfiguration: If entry or exit falls inside the
                reserved "42" pattern cells.
        Returns:
            None
        """
        centre_y = int((self.map.height) / 2)
        centre_x = int((self.map.width) / 2)
        blocked_cells: list[tuple[int, int]]
        blocked_cells = [(-2, -3), (-1, -3), (0, -3), (0, -2), (0, -1),
                         (1, -1), (2, -1), (-2, 1), (-2, 2), (-2, 3),
                         (-1, 3), (0, 3), (0, 2), (0, 1), (1, 1), (2, 1),
                         (2, 2), (2, 3)]
        for y, x in blocked_cells:
            cell_y = centre_y + y
            cell_x = centre_x + x
            cell = self.map.table[cell_y][cell_x]
            if cell.entry or cell.exit:
                raise InvalidConfiguration("Entry or exit inside "
                                           "cells reserved for the 42")
            cell.block()

    def generate(self) -> None:
        """
        Generate a complete maze using recursive backtracking.
        This method:
        - Initializes the grid
        - Applies the "42" pattern if applicable
        - Generates a perfect maze using DFS backtracking
        - Optionally modifies it if a non-perfect maze is required
        - Resets visitation state
        Returns:
            None
        """
        stack: list[Cell] = []
        self.map.gen_map()
        if self.map.height >= 9 and self.map.width >= 11:
            self.block_42_cells()
        if self.map.ind_seed:
            random.seed(self.map.seed)
        else:
            random.seed(None)
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
        self.reset_visited()
        if self.map.perfect is False:
            self.not_perfect()

    def not_perfect(self) -> None:
        """
        Introduce cycles into a perfect maze to make it non-perfect.
        Randomly breaks walls between cells depending on maze size,
        ensuring multiple possible paths between entry and exit.
        Returns:
            None
        """
        break_walls: int = 0
        possible_walls: list[tuple[Cell, Cell, str]] = list()
        size: int = self.map.height * self.map.width
        entry_cell = self.map.table[self.map.entry_y][self.map.entry_x]
        exit_cell = self.map.table[self.map.exit_y][self.map.exit_x]
        neighbors_entry = self.map.get_neighbors(entry_cell)
        for neighbor, direction in neighbors_entry:
            if neighbor == exit_cell:
                for neighbor, direction in neighbors_entry:
                    self.map.connect(entry_cell, neighbor, direction)
                neighbors_exit = self.map.get_neighbors(exit_cell)
                for neighbor, direction in neighbors_exit:
                    self.map.connect(exit_cell, neighbor, direction)
        if size < 10:
            break_walls = 1
        elif size < 100:
            break_walls = 3
        elif size < 300:
            break_walls = int(size / 20)
        else:
            break_walls = int(size / 20)
        for row in self.map.table:
            for cell in row:
                if cell.entry or cell.exit:
                    continue
                else:
                    neighbors = self.map.get_neighbors(cell)
                    neighbors = self.map.get_walled_neighbors(cell, neighbors)
                    for neighbor, direction in neighbors:
                        possible_walls.append((cell, neighbor, direction))
        for _ in range(break_walls):
            if possible_walls:
                index = random.randint(0, len(possible_walls) - 1)
                cell, neighbor, direction = possible_walls.pop(index)
                self.map.connect(cell, neighbor, direction)

    def reset_visited(self) -> None:
        """
        Reset visitation state for all cells in the maze.
        Used after generation and solving phases.
        Returns:
            None
        """
        for row in self.map.table:
            for cell in row:
                cell.unvisit()

    def output(self, direction_list: list[str]) -> None:
        """
        Write the maze and solution to the output file.
        Output format:
        - Hex representation of each cell row by row
        - Blank line
        - Entry coordinates
        - Exit coordinates
        - Shortest path as a sequence of directions
        Args:
            direction_list (list[str]): List of directions representing
                the shortest path (N, E, S, W).
        Returns:
            None
        """
        with open(self.map.output_file, "w") as f:
            for row in self.map.table:
                for cell in row:
                    f.write(cell.get_hex())
                f.write("\n")
            f.write("\n")
            f.write(f"{self.map.entry_y},{self.map.entry_x}\n")
            f.write(f"{self.map.exit_y},{self.map.exit_x}\n")
            for i in direction_list:
                f.write(i)

    def find_exit(self) -> None:
        """
        Find the shortest path between entry and exit using BFS.
        Computes the shortest path in the maze, reconstructs it using
        parent pointers, and writes the result to the output file.
        Returns:
            None
        """
        entry_cell = self.map.table[self.map.entry_y][self.map.entry_x]
        exit_cell = self.map.table[self.map.exit_y][self.map.exit_x]
        queue = [entry_cell]
        entry_cell.visit()
        while queue:
            current_cell = queue.pop(0)
            if current_cell is exit_cell:
                break
            neighbors = self.map.get_neighbors(current_cell)
            unwalled_neighbors = self.map.get_unwalled_neighbors(current_cell,
                                                                 neighbors)
            for neighbor in unwalled_neighbors:
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
        self.output(direction_list)
