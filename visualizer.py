from map import Map

def visualizer(map: Map) -> None:
    for cells in map.table:
        for i in range(len(cells)):
            if (cells[i].north_wall and cells[i].west_wall):
                print("#", end="")
            else:
                print(" ", end="")
            if cells[i].north_wall:
                print("#", end="")
            else:
                print(" ", end="")
        print("#")
        for i in range(len(cells)):
            if cells[i].west_wall:
                print("#", end="")
            else:
                print(" ", end="")
            print(" ", end="")
        print("#")
    for cells in map.table[0]:
        print("##", end="")
    print("#")




