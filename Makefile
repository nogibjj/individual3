install:
	pip install --upgrade pip && \
		pip install -r requirements.txt

test:
	@FILES=$$(find . -name 'test_*.py'); \
	if [ -n "$$FILES" ]; then \
		python -m pytest -vv --cov=main --cov-report=term-missing $$FILES; \
	else \
		echo "No test_*.py files found, skipping tests."; \
	fi

format:
	black .

lint:
	find . -name '*.py' | xargs pylint --disable=R,C

all: install lint test format
