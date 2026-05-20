from parser import parser
from errors import InvalidConfiguration, EmptyFile
import sys
from map import Map
from map_generator import MapGenerator


def main():
    config: dict[str, str]
    if len(sys.argv) == 2:
        try:
            config = parser(sys.argv[1])
            map = Map(config)
            generator = MapGenerator(map)
            generator.generate()
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except PermissionError as e:
            print(f"Error opening file: {e}")
        except InvalidConfiguration as e:
            print(f"Invalid configuration: {e}")
        except EmptyFile as e:
            print(e)
    else:
        print("Error in arguments provided. Usage: python3 a_maze_ing.py <config.txt>")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Something unexpected happened: {e}. Contact developers")
