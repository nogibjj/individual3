install:
	pip install --upgrade pip && \
		pip install -r requirements.txt

pylint:
	@echo "Running pylint..."
	pylint --disable=astroid-error src/

flake8:
	@echo "Running flake8..."
	flake8 .

black-check:
	@echo "Running black check..."
	black .

# isort-check:
#	@echo "Running isort check..."
#	isort --check-only .

format:
	@echo "Running black to format code..."
	black .

lint: pylint flake8 black-check

test:
	@echo "Running tests with pytest..."
	pytest

all: install format lint test
