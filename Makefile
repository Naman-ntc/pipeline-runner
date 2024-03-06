.PHONY: test lint format clean

test:
	pytest -v

lint:
	flake8 .
	mypy .

format:
	black .
	isort .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage .mypy_cache
