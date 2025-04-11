install:
	poetry install

test:
	poetry run pytest -s

coverage:
	poetry run pytest --cov=typo_modal --cov-report=xml

build:
	poetry build

clean:
	rm -rf dist

parquet:
	python3 bin/parquet.py
