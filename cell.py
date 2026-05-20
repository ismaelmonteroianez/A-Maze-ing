class Cell():
    x: int
    y: int
    north_wall: bool
    east_wall: bool
    south_wall: bool
    west_wall: bool
    visited: bool

    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x
        self.north_wall = True
        self.east_wall = True
        self.south_wall = True
        self.west_wall = True
        self.visited = False

    def open_wall(self, position: str) -> None:
        match position:
            case "N":
                self.north_wall = False
            case "E":
                self.east_wall = False
            case "S":
                self.south_wall = False
            case "W":
                self.west_wall = False
            case _:
                raise Exception(f"This direction doesnt exist: {position}")

    def close_wall(self, position: str) -> None:
        match position:
            case "N":
                self.north_wall = True
            case "E":
                self.east_wall = True
            case "S":
                self.south_wall = True
            case "W":
                self.west_wall = True
            case _:
                raise Exception(f"This direction doesnt exist: {position}")

    def get_wall(self, position: str) -> bool:
        match position:
            case "N":
                return self.north_wall
            case "E":
                return self.east_wall
            case "S":
                return self.south_wall
            case "W":
                return self.west_wall
            case _:
                raise Exception(f"This direction doesnt exist: {position}")

    def visit(self) -> None:
        self.visited = True

    def unvisit(self) -> None:
        self.visited = False

    def __repr__(self) -> str:
        return f"({self.y},{self.x})"
