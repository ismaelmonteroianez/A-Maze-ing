from cell import Cell


class Map():
    width: int
    height: int
    entry_y: int
    entry_x: int
    exit_y: int
    exit_x: int
    output_file: str
    perfect: bool
    table: list[list[Cell]]

    def __init__(self, config: dict[str, str]):
        self.width = int(config["WIDTH"])
        self.height = int(config["HEIGHT"])
        parametros = config["ENTRY"].split(",")
        self.entry_y = int(parametros[0])
        self.entry_x = int(parametros[1])
        parametros = config["EXIT"].split(",")
        self.exit_y = int(parametros[0])
        self.exit_y = int(parametros[1])
        self.output_file = config["OUTPUT_FILE"]
        if config["PERFECT"] == "True":
            self.perfect = True
        else:
            self.perfect = False
        self.table = []

    def gen_map(self) -> None:
        self.table = []
        for y in range(self.height):
            new_list = []
            for x in range(self.width):
                new_list.append(Cell(y, x))
            self.table.append(new_list)

    def get_cell(self, x, y) -> Cell:
        return (self.table[y][x])

    def get_neighbors(self, cell: Cell) -> list[tuple[Cell, str]]:
        neighbors = []
        if cell.y > 0:
            neighbors.append((self.table[cell.y - 1][cell.x], "N"))
        if cell.x < self.width - 1:
            neighbors.append((self.table[cell.y][cell.x + 1], "E"))
        if cell.y < self.height - 1:
            neighbors.append((self.table[cell.y + 1][cell.x], "S"))
        if cell.x > 0:
            neighbors.append((self.table[cell.y][cell.x - 1], "W"))
        return neighbors

    def get_unvisited_neighbors(self, neighbors: list[tuple[Cell, str]]) -> list[tuple[Cell, str]]:
        unvisited_neighbors = []
        for cell, direction in neighbors:
            if cell.visited is False:
                unvisited_neighbors.append((cell, direction))
        return (unvisited_neighbors)

    def connect(self, a: Cell, b: Cell, direction: str):
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

    def print_map(self):
        for y in range(self.height):
            for x in range(self.width):
                print(self.table[y][x], end="")
            print()
