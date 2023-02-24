up:

	python src/ceramics/app.py

test:
	pytest --tb=short tests/unit

test-e2e:
	pytest --tb=short tests/e2e

watch-tests:
	ls *.py | entr pytest --tb=short

format:
	isort --profile black .
	black -l 86 $$(find * -name '*.py')