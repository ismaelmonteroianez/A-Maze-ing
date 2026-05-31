class Cell():
    """
    Represent a single cell within the maze.

    A cell stores its coordinates, wall states, traversal metadata,
    and special properties such as entry, exit, or blocked status.
    """
    entry: bool
    exit: bool
    x: int
    y: int
    north_wall: bool
    east_wall: bool
    south_wall: bool
    west_wall: bool
    visited: bool
    father: "Cell"
    blocked: bool

    def __init__(self, y: int, x: int):
        """
        Initialize a maze cell with all walls closed.

        Args:
            y (int): Row coordinate of the cell.
            x (int): Column coordinate of the cell.

        Returns:
            None
        """
        self.entry = False
        self.exit = False
        self.y = y
        self.x = x
        self.north_wall = True
        self.east_wall = True
        self.south_wall = True
        self.west_wall = True
        self.visited = False
        self.father: Cell
        self.blocked = False

    def open_wall(self, position: str) -> None:
        """
        Open a wall of the cell in the specified direction.
        Args:
            position (str): Direction of the wall to open.
                Must be one of "N", "E", "S" or "W".
        Returns:
            None
        Raises:
            Exception: If the specified direction is invalid.
        """
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
        """
        Close a wall of the cell in the specified direction.
        Args:
            position (str): Direction of the wall to close.
                Must be one of "N", "E", "S" or "W".
        Returns:
            None
        Raises:
            Exception: If the specified direction is invalid.
        """
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
        """
        Get the state of a wall in the specified direction.
        Args:
            position (str): Direction of the wall to query.
                Must be one of "N", "E", "S" or "W".
        Returns:
            bool: True if the wall is closed, False otherwise.
        Raises:
            Exception: If the specified direction is invalid.
        """
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

    def get_hex(self) -> str:
        """
        Convert the cell wall configuration to its hexadecimal encoding.
        The encoding follows the project specification:
        North=1, East=2, South=4, West=8.
        Returns:
            str: Hexadecimal digit representing the cell walls.
        """
        result = 0
        hex_value = ("0", "1", "2", "3", "4",
                     "5", "6", "7", "8", "9",
                     "A", "B", "C", "D", "E", "F")
        if self.north_wall:
            result += 1
        if self.east_wall:
            result += 2
        if self.south_wall:
            result += 4
        if self.west_wall:
            result += 8
        return hex_value[result]

    def visit(self) -> None:
        """
        Mark the cell as visited.
        Returns:
        None
        """
        self.visited = True

    def unvisit(self) -> None:
        """
        Mark the cell as not visited.
        Returns:
            None
        """
        self.visited = False

    def __repr__(self) -> str:
        """
        Return a string representation of the cell coordinates.
        Returns:
            str: Cell coordinates formatted as '(y,x)'.
        """
        return f"({self.y},{self.x})"

    def block(self) -> None:
        """
        Mark the cell as blocked.
        Blocked cells are excluded from the traversable maze and may be
        used to form the required '42' pattern.
        Returns:
            None
        """
        self.blocked = True
