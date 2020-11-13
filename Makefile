install:
	@poetry install

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest -v --verbose --cov=page_loader tests/

selfcheck:
	poetry check

check: selfcheck lint test

build: check
	poetry build

.PHONY: install lint test selfcheck check build publish