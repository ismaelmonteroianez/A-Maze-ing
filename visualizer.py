from map import Map

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
                
