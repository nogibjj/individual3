install:
	python -m pip install --upgrade pip && \
	python -m pip install -r requirements.txt


test:
	@FILES=$$(find . -name 'test_*.py'); \
	if [ -n "$$FILES" ]; then \
		python -m pytest -vv --cov=main --cov-report=term-missing $$FILES; \
	else \
		echo "No test_*.py files found, skipping tests."; \
	fi

format:
	black --line-length 79 . && \
	isort --profile black .


lint:
	@echo "Running pylint..."
	find . -name '*.py' | xargs pylint --disable=R,C

	@echo "Running flake8..."
	flake8 .

all: install format lint test
