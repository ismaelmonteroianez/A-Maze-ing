from errors import InvalidConfiguration, EmptyFile


def check_int(value:str) -> None:
    num = int(value)
    if num <= 0:
        raise InvalidConfiguration("El valor no puede ser negativo o 0")

def check_cord(value:str) -> None:
    cordenadas = value.split(",")
    if len(cordenadas) == 2:
        for cordenada in cordenadas:
            num = int(cordenada)
            if num < 0:
                raise InvalidConfiguration("El valor no puede ser negativo")
    else:
        raise InvalidConfiguration("Cordenada invalida")

def check_file(value:str) -> None:
    with open(value, "w") as f:
        f.write("Hola")


def check_bool(value:str):
    if not (value == "True" or value == "False"):
        raise InvalidConfiguration(f"{value} must be True or False only")


def check_invalid_cord(config:dict[str,str]) -> None:
    width:int = int(config["WIDTH"])
    height:int = int(config["HEIGHT"])
    entry:list[str] = config["ENTRY"].split(",")
    width_entry:int = int(entry[0])
    height_entry:int = int(entry[1])
    exit:list[str] = config["EXIT"].split(",")
    width_exit:int = int(exit[0])
    height_exit:int = int(exit[1])

    if entry == exit:
        raise InvalidConfiguration("ENTRY and EXIT must not be the same")
    if (width <= width_entry or width <= width_exit):
        raise InvalidConfiguration("Cordenada incorrecta")
    if (height <= height_entry or height <= height_exit):
        raise InvalidConfiguration("Cordenada incorrecta")
    



def parser(argv:str) -> dict[str, str]:
    mandatory_keys = {"WIDTH":"int",
                      "HEIGHT":"int",
                      "ENTRY":"cord",
                      "EXIT":"cord",
                      "OUTPUT_FILE":"file",
                      "PERFECT":"bool"}
    config = {}
    with open(argv, "r") as f:
        file = f.read()
    if file.strip() == "":
        raise EmptyFile("Error: empty file")
    lines = file.split("\n")
    for line in lines:
        parameter = line.split("=")
        if len(parameter) == 2:
            if parameter[0] in config:
                raise InvalidConfiguration(f"repeated key in parameter {parameter[0]}")
            config[parameter[0].upper()] = parameter[1]
        else:
            raise InvalidConfiguration(f"number of parameters must be 2, you had {len(parameter)}")
    for key in mandatory_keys:
        if key in config.keys():
            try:
                match mandatory_keys[key]:
                    case "int":
                        check_int(config[key])
                    case "cord":
                        check_cord(config[key])
                    case "file":
                        check_file(config[key])
                    case "bool":
                        check_bool(config[key])
            except Exception as e:
                raise InvalidConfiguration(e)
        else:
            raise InvalidConfiguration(f"Son obligatorias las siguientes argumentos {mandatory_keys.keys()}")
    check_invalid_cord(config)
    return config
