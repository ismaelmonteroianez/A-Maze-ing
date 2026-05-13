from a_maze_ing.errors import InvalidConfiguration, EmptyFile

def parser() -> dict[str, str]:
    config = {}
    with open("config.txt", "r") as f:
        file = f.read()
    if file.strip() == "":
        raise EmptyFile("Error: empty file")
    lines = file.split("\n")
    print(lines)
    for line in lines:
        parameter = line.split("=")
        if len(parameter) == 2:
            if parameter[0] in config:
                raise InvalidConfiguration(f"repeated key in parameter {parameter[0]}")
            config[parameter[0]] = parameter[1]
        else:
            raise InvalidConfiguration(f"number of parameters must be 2, you had {len(parameter)}")
