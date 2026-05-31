.PHONY: all install run debug build clean fclean re lint lint-strict

CONFIG=config.txt

all:
	@echo "Available targets: install run debug lint clean"

install:
	python3 -m pip install flake8 mypy build

run:
	python3 a_maze_ing.py $(CONFIG)

debug:
	python3 -m pdb a_maze_ing.py $(CONFIG)

build:
	python3 -m build

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

lint-strict:
	python3 -m flake8 .
	python3 -m mypy . --strict

clean:
	rm -rf __pycache__/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

fclean: clean
	rm -f maze.txt

re: fclean run