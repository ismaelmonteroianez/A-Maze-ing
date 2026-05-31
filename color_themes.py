"""
Color theme system for maze visualization.

This module defines multiple ANSI color themes used to render
the maze in the terminal, including special coloring for walls,
paths, entry/exit points, and the "42" pattern.
"""


class ColorThemes:
    """
    Manage multiple ANSI color themes for maze rendering.
    This class stores a collection of visual themes used to display
    the maze in the terminal. It supports cycling through themes
    and provides a special color rotation for the "42" pattern.
    """
    def __init__(self) -> None:
        """
        Initialize the color theme manager.
        Loads predefined color themes and initializes indices used
        for cycling through visual styles.
        Returns:
            None
        """
        self.index = 0

        self.themes = [
            {
                "wall": self.color("██", 97),
                "empty": "  ",
                "path": self.color("██", 90),
                "entry": self.color("██", 92),
                "exit": self.color("██", 91),
                "forty_two": self.color("██", 95),
            },

            {
                "wall": self.color("██", 94),
                "empty": "  ",
                "path": self.color("██", 96),
                "entry": self.color("██", 93),
                "exit": self.color("██", 91),
                "forty_two": self.color("██", 95),
            },

            {
                "wall": self.color("██", 92),
                "empty": "  ",
                "path": self.color("██", 97),
                "entry": self.color("██", 94),
                "exit": self.color("██", 91),
                "forty_two": self.color("██", 93),
            },

            {
                "wall": self.color("██", 97),
                "empty": "  ",
                "path": self.color("██", 90),
                "entry": self.color("██", 92),
                "exit": self.color("██", 91),
                "forty_two": self.color("██", 95),
            },


            {
                "wall": self.color("██", 94),
                "empty": "  ",
                "path": self.color("██", 96),
                "entry": self.color("██", 92),
                "exit": self.color("██", 91),
                "forty_two": self.color("██", 95),
            },


            {
                "wall": self.color("██", 32),
                "empty": "  ",
                "path": self.color("██", 92),
                "entry": self.color("██", 96),
                "exit": self.color("██", 91),
                "forty_two": self.color("██", 33),
            },


            {
                "wall": self.color("██", 91),
                "empty": "  ",
                "path": self.color("██", 93),
                "entry": self.color("██", 97),
                "exit": self.color("██", 95),
                "forty_two": self.color("██", 31),
            },


            {
                "wall": self.color("██", 95),
                "empty": "  ",
                "path": self.color("██", 94),
                "entry": self.color("██", 96),
                "exit": self.color("██", 91),
                "forty_two": self.color("██", 97),
            },


            {
                "wall": self.color("██", 32),
                "empty": "  ",
                "path": self.color("██", 92),
                "entry": self.color("██", 97),
                "exit": self.color("██", 91),
                "forty_two": self.color("██", 90),
            },


            {
                "wall": self.color("██", 96),
                "empty": "  ",
                "path": self.color("██", 97),
                "entry": self.color("██", 94),
                "exit": self.color("██", 91),
                "forty_two": self.color("██", 90),
            },


            {
                "wall": self.color("██", 93),
                "empty": "  ",
                "path": self.color("██", 91),
                "entry": self.color("██", 95),
                "exit": self.color("██", 31),
                "forty_two": self.color("██", 97),
            },


            {
                "wall": self.color("██", 95),
                "empty": "  ",
                "path": self.color("██", 96),
                "entry": self.color("██", 93),
                "exit": self.color("██", 92),
                "forty_two": self.color("██", 91),
            },


            {
                "wall": self.color("██", 90),
                "empty": "  ",
                "path": self.color("██", 37),
                "entry": self.color("██", 92),
                "exit": self.color("██", 91),
                "forty_two": self.color("██", 93),
            },


            {
                "wall": self.color("██", 95),
                "empty": "  ",
                "path": self.color("██", 93),
                "entry": self.color("██", 96),
                "exit": self.color("██", 91),
                "forty_two": self.color("██", 92),
            },


            {
                "wall": self.color("██", 37),
                "empty": "  ",
                "path": self.color("██", 90),
                "entry": self.color("██", 97),
                "exit": self.color("██", 91),
                "forty_two": self.color("██", 30),
            }
        ]

        self.forty_two_colors = [
            self.color("██", 95),
            self.color("██", 93),
            self.color("██", 96),
            self.color("██", 92),
            self.color("██", 91),
            self.color("██", 37),
        ]

        self.forty_two_index = 0

    def color(self, text: str, code: int) -> str:
        """
        Apply ANSI color formatting to a text string.
        Args:
            text (str): Text to be colored.
            code (int): ANSI color code.
        Returns:
            str: Colored text string with ANSI escape sequences.
        """
        return f"\033[{code}m{text}\033[0m"

    def current(self) -> dict[str, str]:
        """
        Get the current active color theme.
        Returns a copy of the active theme, with the "42" color
        dynamically selected from its rotation palette.
        Returns:
            dict[str, str]: Dictionary containing color mappings
                for wall, empty space, path, entry, exit, and
                "forty_two".
        """
        theme = self.themes[self.index].copy()
        theme["forty_two"] = (self.forty_two_colors[self.forty_two_index])
        return theme

    def next_theme(self) -> None:
        """
        Switch to the next available color theme.
        Cycles through predefined themes in a circular manner.
        Returns:
            None
        """
        self.index += 1
        if self.index >= len(self.themes):
            self.index = 0

    def next_42_theme(self) -> None:
        """
        Cycle to the next color used for the "42" pattern.
        This affects only the special coloring used to render the
        blocked cells forming the "42" shape.
        Returns:
            None
        """
        self.forty_two_index += 1
        if self.forty_two_index >= len(self.forty_two_colors):
            self.forty_two_index = 0
