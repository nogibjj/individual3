install:
	pip install --upgrade pip && \
		pip install -r requirements.txt

pylint:
	@echo "Running pylint..."
	pylint --disable=R,C,W --disable=astroid-error src/

flake8:
	@echo "Running flake8..."
	flake8 .

# isort-check:
#	@echo "Running isort check..."
#	isort --check-only .

lint: pylint flake8

format:
	@echo "Running black to format code..."
	black .

test:
	@echo "Running tests with pytest..."
	pytest

all: install format lint test
