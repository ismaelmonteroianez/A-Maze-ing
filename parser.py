from errors import InvalidConfiguration, EmptyFile
"""
Parse and validate maze configuration files.

This module reads configuration files, validates required and
optional parameters, and returns a dictionary containing the
parsed configuration values.
"""


def check_int(value: str) -> None:
    """
    Validate that a value is a positive integer.
    Args:
        value (str): Value to validate.
    Returns:
        None
    Raises:
        InvalidConfiguration: If the value is not positive.
        ValueError: If the value cannot be converted to an integer.
    """
    num = int(value)
    if num <= 0:
        raise InvalidConfiguration("Value must be positive")


def check_cord(value: str) -> None:
    """
    Validate a coordinate pair.
    Coordinates must be provided in the format "y,x" and both
    values must be non-negative integers.
    Args:
        value (str): Coordinate string to validate.
    Returns:
        None
    Raises:
        InvalidConfiguration: If the coordinate format or values
            are invalid.
        ValueError: If coordinates cannot be converted to integers.
    """
    cordenadas = value.split(",")
    if len(cordenadas) == 2:
        for cordenada in cordenadas:
            num = int(cordenada)
            if num < 0:
                raise InvalidConfiguration("Value must be positive")
    else:
        raise InvalidConfiguration("Invalid coordinate")


def check_file(value: str) -> None:
    """
    Validate that an output file can be created or written.
    Args:
        value (str): Output file path.
    Returns:
        None
    Raises:
        OSError: If the file cannot be opened for writing.
    """
    with open(value, "w"):
        pass


def check_bool(value: str) -> None:
    """
    Validate a boolean configuration value.
    Accepted values are "TRUE" and "FALSE", regardless of case.
    Args:
        value (str): Value to validate.
    Returns:
        None
    Raises:
        InvalidConfiguration: If the value is not a valid boolean.
    """
    if not (value.upper() == "TRUE" or value.upper() == "FALSE"):
        raise InvalidConfiguration(f"{value} must be True or False only")


def check_invalid_cord(config: dict[str, str]) -> None:
    """
    Validate maze dimensions and entry/exit coordinates.
    Ensures that coordinates are inside maze bounds, that entry
    and exit positions are different, and that maze dimensions
    respect the configured limits.
    Args:
        config (dict[str, str]): Parsed configuration values.
    Returns:
        None
    Raises:
        InvalidConfiguration: If dimensions or coordinates are
            invalid.
    """
    width: int = int(config["WIDTH"])
    height: int = int(config["HEIGHT"])
    entry: list[str] = config["ENTRY"].split(",")
    height_entry: int = int(entry[0])
    width_entry: int = int(entry[1])
    exit: list[str] = config["EXIT"].split(",")
    height_exit: int = int(exit[0])
    width_exit: int = int(exit[1])

    if entry == exit:
        raise InvalidConfiguration("ENTRY and EXIT must not be the same")
    if (width <= width_entry or width <= width_exit):
        raise InvalidConfiguration("Invalid coordinate")
    if (height <= height_entry or height <= height_exit):
        raise InvalidConfiguration("Invalid coordinate")
    if width > 100:
        raise InvalidConfiguration("Width must be less than 100")
    if height > 100:
        raise InvalidConfiguration("Height must be less than 100")


def parser(argv: str) -> dict[str, str]:
    """
    Parse and validate a maze configuration file.
    Reads the configuration file, validates all required and
    optional parameters, and returns the resulting configuration
    dictionary.
    Args:
        argv (str): Path to the configuration file.
    Returns:
        dict[str, str]: Validated configuration values.
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        EmptyFile: If the configuration file is empty.
        InvalidConfiguration: If any configuration parameter is
            missing or invalid.
    """
    mandatory_keys = {"WIDTH": "int",
                      "HEIGHT": "int",
                      "ENTRY": "cord",
                      "EXIT": "cord",
                      "OUTPUT_FILE": "file",
                      "PERFECT": "bool"}
    optional_keys = {"SEED": "str"}
    config: dict[str, str] = {}
    with open(argv, "r") as f:
        file = f.read()
    if file.strip() == "":
        raise EmptyFile("Error: empty file")
    lines = file.split("\n")
    for line in lines:
        parameter = line.split("=")
        if len(parameter) == 2:
            if parameter[0] in config:
                raise InvalidConfiguration("repeated key "
                                           f"in parameter {parameter[0]}")
            config[parameter[0].upper()] = parameter[1]
        else:
            raise InvalidConfiguration("number of parameters "
                                       f"must be 2, you had {len(parameter)}")
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
                        config[key] = (config[key]).upper()
            except Exception as e:
                raise InvalidConfiguration(e)
        else:
            raise InvalidConfiguration("The following arguments are "
                                       f"mandatory: {mandatory_keys.keys()}")
    for key in optional_keys:
        if key in config.keys():
            try:
                match optional_keys[key]:
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
    check_invalid_cord(config)
    return config
