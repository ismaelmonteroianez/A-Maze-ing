from parser import parser
from errors import InvalidConfiguration, EmptyFile


def main():
    try:
        parser()
    except FileNotFoundError as e:
        print(f"File not found: {e}") 
    except PermissionError as e:
        print(f"Error opening file: {e}")
    except InvalidConfiguration as e:
        print(f"Invalid configuration: {e}")
    except EmptyFile as e:
        print(e)

if __name__ == "__main__":
    try: 
        main()
    except Exception as e:
        print(f"Something unexpected happened: {e}. Contact developers")
