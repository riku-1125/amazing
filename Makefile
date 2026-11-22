PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt
VENV = .venv
VPY = $(VENV)/bin/python
VPIP = $(VENV)/bin/pip

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m venv $(VENV)
	$(VPIP) install -r requirements.txt

run:
	$(VPY) $(MAIN) $(CONFIG)

debug:
	$(VPY) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	$(VPY) -m flake8 . --exclude $(VENV)
	$(VPY) -m mypy . --exclude $(VENV) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(VPY) -m flake8 . --exclude $(VENV)
	$(VPY) -m mypy --strict . --exclude $(VENV)
