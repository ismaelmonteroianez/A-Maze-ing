from parser import parser
from errors import InvalidConfiguration, EmptyFile
import sys
from map import Map


def main():
    config:dict[str,str]
    if len(sys.argv) == 2:
        try:
            config = parser(sys.argv[1])
            map = Map(config)
            map.gen_map()
            map.print_map()
        except FileNotFoundError as e:
            print(f"File not found: {e}") 
        except PermissionError as e:
            print(f"Error opening file: {e}")
        except InvalidConfiguration as e:
            print(f"Invalid configuration: {e}")
        except EmptyFile as e:
            print(e)
    else:
        print("El programa tiene que ejecutarse asi: python3 a_maze_ing.py <argumento>")

if __name__ == "__main__":
    try: 
        main()
    except Exception as e:
        print(f"Something unexpected happened: {e}. Contact developers")
    