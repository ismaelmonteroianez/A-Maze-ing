from map import Map
from map_generator import MapGenerator


def visualizer(map: Map) -> None:
    for cell in map.table[0]:
        print("+", end="")
        print("---", end="")
    print("+")
    for row in map.table:
        print("|", end="")
        for cell in row:
            if cell.entry:
                print(" E ", end="")
            elif cell.exit:
                print(" S ", end="")
            elif cell.visited:
                print(" * ", end="")
            else:
                print("   ", end="")
            if cell.east_wall:
                print("|", end="")
            else:
                print(" ", end="")
        print()
        print("+", end="")
        for cell in row:
            if cell.south_wall:
                print("---", end="")
            else:
                print("   ", end="")
            print("+", end="")
        print()

def canvas(map: Map, show_path: bool) -> None:
    canvas_height = map.height * 2 + 1
    canvas_width = map.width * 2 + 1
    wall = "██"
    empty = "  "
    path = "\033[90m██\033[0m"
    entry = "\033[92m██\033[0m"
    exit = "\033[91m██\033[0m"
    forty_two = "\033[95m██\033[0m"
    canvas = []
    for _ in range(canvas_height):
        canvas.append([wall] * canvas_width)
    for y in range(map.height):
        for x in range(map.width):
            cell = map.table[y][x]
            cy = y * 2 + 1
            cx = x * 2 + 1
            if cell.entry:
                canvas[cy][cx] = entry
            elif cell.exit:
                canvas[cy][cx] = exit
            elif cell.blocked:
                canvas[cy][cx] = forty_two
            elif cell.visited and show_path:
                    canvas[cy][cx] = path
            else:
                canvas[cy][cx] = empty
            if not cell.east_wall:
                neighbor = map.table[y][x + 1]
                if cell.visited and neighbor.visited and show_path:
                    canvas[cy][cx + 1] = path
                else:    
                    canvas[cy][cx + 1] = empty
            if not cell.south_wall:
                neighbor = map.table[y + 1][x]
                if cell.visited and neighbor.visited and show_path:
                    canvas[cy + 1][cx] = path
                else:
                    canvas[cy + 1][cx] = empty
            
    for row in canvas:
        print("".join(row))

def menu(config: dict[str,str]):
    show_path = True
    map = Map(config)
    generator = MapGenerator(map)
    generator.generate()
    generator.find_exit()
    
    while True:
        print("\033[H\033[J", end="") #Limpia la pantalla para que cuando se genere un nuevo laberinto que no haya nada arriba en la terminal
        canvas(map, show_path)
        if map.height < 9 or map.width < 11:
            print("Maze too small to generate pattern 42. Generating map anyway:")
        print("==== A-Maze-ing ====")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Toggle 42 pattern colours")
        print("5. Tool seed")
        print("6. Exit")
        print()

        choice = input("Choice? (1-6): ")

        if choice == "1":
            generator.generate()
            generator.find_exit()

        elif choice == "2":
            show_path = not show_path

        elif choice == "3":
            print("Change colours selected")

        elif choice == "4":
            print("42 pattern selected")

        elif choice == "5":
            if generator.map.ind_seed:
                generator.map.ind_seed = False
            else:
                if generator.map.empty_seed:
                    generator.map.seed = input("Seed not found. Insert Seed: ")
                    generator.map.empty_seed = False
                generator.map.ind_seed = True
            generator.generate()
            generator.find_exit()

        elif choice == "6":
            break

        else:
            print("Invalid option")

        input("\nPress ENTER to continue...")