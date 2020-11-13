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

publish: build
	poetry publish -r test_pypi

.PHONY: install lint test selfcheck check build publish