from parser import parser
from errors import InvalidConfiguration, EmptyFile
import sys
from visualizer import menu


def main() -> None:
    """
    Parse the configuration file and start the maze application.

    Validates the command-line arguments, loads the configuration file,
    and launches the interactive menu. Handles expected configuration
    and file-related errors by displaying a user-friendly message.

    Returns:
        None
    """
    config: dict[str, str]
    if len(sys.argv) == 2:
        try:
            config = parser(sys.argv[1])
            menu(config)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except PermissionError as e:
            print(f"Error opening file: {e}")
        except InvalidConfiguration as e:
            print(f"Invalid configuration: {e}")
        except EmptyFile as e:
            print(e)
    else:
        print("Error in arguments provided."
              " Usage: python3 a_maze_ing.py <config.txt>")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Something unexpected happened: {e}. Contact developers")
