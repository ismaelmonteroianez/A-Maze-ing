# *This project has been created as part of the 42 curriculum by ismonter, davgarc4.*

# A-Maze-ing

A-Maze-ing is a maze generator written in Python capable of generating both perfect and imperfect mazes from a configuration file.
The project includes:

* Random maze generation with optional reproducibility through seeds
* Hexadecimal maze export format
* Terminal visual rendering with interactive controls
* Shortest path solving
* Reusable maze generation package (`mazegen`)
* Customizable color themes
* Embedded “42” pattern generation

---

# Description

The goal of this project is to generate coherent and fully connected mazes while respecting a strict file format and multiple structural constraints.

Each maze cell contains four possible walls:

* North
* East
* South
* West

The generated maze can either be:

* **Perfect** → exactly one valid path exists between entry and exit
* **Imperfect** → additional random walls are removed to create multiple possible paths

The program also exports the maze into a hexadecimal representation and provides a visual interactive terminal renderer.

---

# Features

* Configurable maze dimensions
* Perfect and imperfect maze generation
* Deterministic generation using seeds
* BFS shortest path solving
* ASCII terminal visualization
* Interactive menu system
* Multiple color themes
* Toggleable shortest path display
* Embedded “42” pattern using blocked cells
* Reusable `mazegen` package architecture
* Hexadecimal export format

---

# Instructions

## Execution

```bash
python3 a_maze_ing.py config.txt
```

Where:

* `a_maze_ing.py` is the main executable
* `config.txt` is the configuration file

---

# Configuration File Format

The configuration file uses the following syntax:

```txt
KEY=VALUE
```

Lines beginning with `#` are ignored.

## Mandatory Keys

| Key         | Description       | Example              |
| ----------- | ----------------- | -------------------- |
| WIDTH       | Maze width        | WIDTH=20             |
| HEIGHT      | Maze height       | HEIGHT=15            |
| ENTRY       | Entry coordinates | ENTRY=0,0            |
| EXIT        | Exit coordinates  | EXIT=19,14           |
| OUTPUT_FILE | Output filename   | OUTPUT_FILE=maze.txt |
| PERFECT     | Perfect maze mode | PERFECT=True         |

## Optional Keys

| Key  | Description            |
| ---- | ---------------------- |
| SEED | Reproducible maze seed |

---

# Example Configuration

```txt
WIDTH=13
HEIGHT=13
ENTRY=0,0
EXIT=12,12
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

---

# Maze Generation Algorithm

## Recursive Backtracking / DFS

The maze generation algorithm is based on an iterative implementation of:

* Recursive Backtracking
* Depth-First Search (DFS)

The algorithm works by:

1. Starting from the entry cell
2. Visiting random neighboring cells
3. Removing walls between connected cells
4. Backtracking when no unvisited neighbors remain

This approach naturally generates perfect mazes with a single valid path between any two cells.

### Why we chose this algorithm

We selected Recursive Backtracking because:

* It is simple and efficient
* Produces visually interesting mazes
* Guarantees full connectivity
* Easily supports reproducibility through seeds
* Integrates naturally with wall-based maze structures

Additionally, its stack-based implementation allowed us to avoid recursion depth limitations.

---

# Imperfect Maze Generation

When `PERFECT=False`, additional random walls are removed after the DFS generation phase.

This creates:

* Multiple valid paths
* More open maze structures
* Less predictable navigation

The amount of removed walls scales with maze size.

---

# Shortest Path Solver

The shortest valid path between the entry and exit is calculated using a second traversal algorithm based on:

* Breadth-First Search (BFS)

The BFS traversal:

* Guarantees the shortest path
* Stores parent references for path reconstruction
* Marks the final path visually inside the renderer
* Exports the solution path to the output file

---

# Output File Format

Each maze cell is encoded as a hexadecimal digit.

## Bit Representation

| Bit | Direction |
| --- | --------- |
| 0   | North     |
| 1   | East      |
| 2   | South     |
| 3   | West      |

Closed walls are represented by `1`.

## Example

```txt
B955179139513
AC3BC56AEC3AA
C3C47938396AA
B81556AEC696E
82AFB92FFF853
A82FC4057FC7A
AAAFFFAFFF952
A8413FAFD503E
AC3AAFAFFFAC3
83AEC3C393852
AAC53C3C6C6BA
AC55696951546
C555545454557

0,0
12,12
SSESESSSSEESSESESWSEEEEEEE
```

The output contains:

1. The maze structure
2. Entry coordinates
3. Exit coordinates
4. Shortest valid path

---

# Visual Representation

The project includes an interactive terminal renderer.

## Available Controls

| Key | Action                     |
| --- | -------------------------- |
| 1   | Generate new maze          |
| 2   | Show / hide shortest path  |
| 3   | Change color theme         |
| 4   | Change “42” pattern colors |
| 5   | Toggle seed mode           |
| 6   | Exit                       |

---

# The “42” Pattern

The maze contains an embedded “42” pattern made from blocked cells.

These cells:

* Are completely inaccessible
* Remain isolated from maze traversal
* Are visually highlighted in the renderer

If the maze dimensions are too small, the pattern is omitted and a warning is displayed.

---

# Reusable Package

The reusable part of the project is located inside:

```txt
mazegen/
```

Current reusable components:

* `Cell`
* `Map`
* `MapGenerator`

The package architecture was designed to allow future installation through `pip`.

---

# Reusable Module Example

```python
from mazegen import MapGenerator

config = {
    "WIDTH": "20",
    "HEIGHT": "20",
    "ENTRY": "0,0",
    "EXIT": "19,19",
    "OUTPUT_FILE": "maze.txt",
    "PERFECT": "TRUE"
}

generator = MapGenerator(config)

generator.generate()
generator.find_exit()
```

---

# Project Structure

```txt
.
├── a_maze_ing.py
├── parser.py
├── visualizer.py
├── color_themes.py
├── errors.py
├── config.txt
├── README.md
└── mazegen/
    ├── cell.py
    ├── map.py
    └── map_generator.py
```

---

# Installation

## Packaging

TODO

## Pip Installation

TODO

---

# Team & Project Management

## Team Workflow

The entire project was developed collaboratively in real time instead of dividing isolated tasks between team members.

This approach allowed us to:

* Debug algorithms together
* Validate maze coherence continuously
* Iterate quickly on architecture decisions

---

## Development Process

The maze generation algorithms worked correctly surprisingly early during development.

The most challenging part of the project was:

* The visual rendering system
* Terminal visualization logic
* Dynamic color rendering
* Interactive controls

Managing visual clarity while preserving maze coherence required several iterations.

---

## Tools Used

* GitHub
* Discord

---

## What Worked Well

* Algorithm implementation
* Data structure organization
* Separation between generation and visualization
* Reusable package architecture

---

## What Could Be Improved

TODO

---

# AI Usage

AI tools were used as auxiliary support for:

* Documentation structuring
* README formatting
* General code review discussions
* Small debugging guidance

All core algorithms, architecture decisions, and implementations were developed manually.

---

# Resources

## Documentation

* Python Official Documentation
* DFS / Recursive Backtracking articles
* BFS shortest path references
* ANSI terminal color documentation

## Additional Resources

TODO

---

# Future Improvements

Possible future additions include:

* Multiple generation algorithms
* Animated generation
* GUI rendering
* Performance optimizations
* Advanced package distribution
* Full docstring documentation

---
