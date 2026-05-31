from mazegen.cell import Cell


class Map():
    """
    Represent the maze structure and provide utility methods to
    manipulate and query its cells.

    The map stores the maze dimensions, entry and exit positions,
    generation settings, and the grid of cells composing the maze.
    """
    width: int
    height: int
    entry_y: int
    entry_x: int
    exit_y: int
    exit_x: int
    output_file: str
    perfect: bool
    seed: str
    empty_seed: bool
    ind_seed: bool
    table: list[list[Cell]]

    def __init__(self, config: dict[str, str]):
        """
        Initialize the maze map from a configuration dictionary.
        Args:
            config (dict[str, str]): Parsed configuration containing
                maze dimensions, entry and exit coordinates, output
                settings and generation options.
        Returns:
            None
        """
        self.width = int(config["WIDTH"])
        self.height = int(config["HEIGHT"])
        parametros = config["ENTRY"].split(",")
        self.entry_y = int(parametros[0])
        self.entry_x = int(parametros[1])
        parametros = config["EXIT"].split(",")
        self.exit_y = int(parametros[0])
        self.exit_x = int(parametros[1])
        self.output_file = config["OUTPUT_FILE"]
        if config["PERFECT"] == "TRUE":
            self.perfect = True
        else:
            self.perfect = False
        if "SEED" in config.keys():
            self.empty_seed = False
            self.ind_seed = True
            self.seed = config["SEED"]
        else:
            self.empty_seed = True
            self.ind_seed = False
        self.table = []

    def gen_map(self) -> None:
        """
        Create and initialize the maze grid.
        Generates a two-dimensional table of cells with all walls
        closed and marks the configured entry and exit cells.
        Returns:
            None
        """
        self.table = []
        for y in range(self.height):
            new_list = []
            for x in range(self.width):
                new_list.append(Cell(y, x))
            self.table.append(new_list)
        self.table[self.entry_y][self.entry_x].entry = True
        self.table[self.exit_y][self.exit_x].exit = True

    def get_neighbors(self, cell: Cell) -> list[tuple[Cell, str]]:
        """
        Get all valid neighboring cells of a given cell.
        Only neighbors within maze bounds and not marked as blocked
        are returned.
        Args:
            cell (Cell): Cell whose neighbors will be retrieved.
        Returns:
            list[tuple[Cell, str]]: List of neighboring cells and their
            relative directions ("N", "E", "S" or "W").
        """
        neighbors = []
        neighbor: Cell
        if cell.blocked is False:
            if cell.y > 0:
                neighbor = self.table[cell.y - 1][cell.x]
                if neighbor.blocked is False:
                    neighbors.append((neighbor, "N"))
            if cell.x < self.width - 1:
                neighbor = self.table[cell.y][cell.x + 1]
                if neighbor.blocked is False:
                    neighbors.append((neighbor, "E"))
            if cell.y < self.height - 1:
                neighbor = self.table[cell.y + 1][cell.x]
                if neighbor.blocked is False:
                    neighbors.append((neighbor, "S"))
            if cell.x > 0:
                neighbor = self.table[cell.y][cell.x - 1]
                if neighbor.blocked is False:
                    neighbors.append((neighbor, "W"))
        return neighbors

    def get_unvisited_neighbors(self, neighbors: list[tuple[Cell, str]]
                                ) -> list[tuple[Cell, str]]:
        """
        Filter a list of neighbors to keep only unvisited cells.
        Args:
            neighbors (list[tuple[Cell, str]]): Neighboring cells and
                their directions.
        Returns:
            list[tuple[Cell, str]]: Unvisited neighboring cells and
            their directions.
        """
        unvisited_neighbors = []
        for cell, direction in neighbors:
            if cell.visited is False:
                unvisited_neighbors.append((cell, direction))
        return (unvisited_neighbors)

    def get_unwalled_neighbors(self, current_cell: Cell,
                               neighbors: list[tuple[Cell, str]]
                               ) -> list[Cell]:
        """
        Get neighboring cells connected to the current cell.
        A neighbor is considered connected when no wall separates it
        from the current cell.
        Args:
            current_cell (Cell): Cell from which connections are checked.
            neighbors (list[tuple[Cell, str]]): Neighboring cells and
                their directions.
        Returns:
            list[Cell]: Connected neighboring cells.
        """
        unwalled_neighbors = []
        for cell, direction in neighbors:
            if direction == "N" and current_cell.north_wall is False:
                unwalled_neighbors.append(cell)
            if direction == "E" and current_cell.east_wall is False:
                unwalled_neighbors.append(cell)
            if direction == "S" and current_cell.south_wall is False:
                unwalled_neighbors.append(cell)
            if direction == "W" and current_cell.west_wall is False:
                unwalled_neighbors.append(cell)
        return (unwalled_neighbors)

    def get_walled_neighbors(self, current_cell: Cell,
                             neighbors: list[tuple[Cell, str]]
                             ) -> list[tuple[Cell, str]]:
        """
        Get neighboring cells separated by a wall.
        Only east and south neighbors are considered to avoid
        duplicate wall checks.
        Args:
            current_cell (Cell): Cell from which walls are checked.
            neighbors (list[tuple[Cell, str]]): Neighboring cells and
                their directions.
        Returns:
            list[tuple[Cell, str]]: Neighboring cells still separated
            by a wall.
        """
        walled_neighbors = []
        for cell, direction in neighbors:
            if direction == "E" and current_cell.east_wall:
                walled_neighbors.append((cell, "E"))
            if direction == "S" and current_cell.south_wall:
                walled_neighbors.append((cell, "S"))
        return walled_neighbors

    def connect(self, a: Cell, b: Cell, direction: str) -> None:
        """
        Create a passage between two adjacent cells.
        Opens the wall in the specified direction for the first cell
        and the corresponding opposite wall for the second cell.
        Args:
            a (Cell): First cell.
            b (Cell): Adjacent cell to connect.
            direction (str): Direction of the connection from the first
                cell ("N", "E", "S" or "W").
        Returns:
            None
        """
        a.open_wall(direction)
        match direction:
            case "N":
                b.open_wall("S")
            case "E":
                b.open_wall("W")
            case "S":
                b.open_wall("N")
            case "W":
                b.open_wall("E")

    def print_map(self) -> None:
        """
        Print the maze grid using the cell string representation.
        This method is intended for debugging purposes.
        Returns:
            None
        """
        for y in range(self.height):
            for x in range(self.width):
                print(self.table[y][x], end="")
            print()
