install:
	pip install --upgrade pip && \
		pip install -r requirements.txt

pylint:
	@echo "Running pylint..."
	find . -name '*.py' | xargs pylint --disable=R,C

flake8:
	@echo "Running flake8..."
	flake8 .

black-check:
	@echo "Running black check..."
	black .

isort-check:
	@echo "Running isort check..."
	isort --check-only .

format:
	@echo "Running black and isort to format code..."
	black . && \
	isort .

lint: pylint flake8 black-check isort-check

test:
	@echo "Running tests with pytest..."
	pytest

all: install format lint test
