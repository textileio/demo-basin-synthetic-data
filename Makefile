setup:
	pipenv shell
	pipenv run pre-commit install -t pre-commit
	pipenv run pre-commit install -t pre-push

install:
	pipenv install --dev

format:
	pipenv run isort --atomic .
	pipenv run black --check .
	pipenv run flake8
	pipenv run mypy

test:
	pipenv run pytest

coverage:
	pipenv run pytest --cov --cov-fail-under=100
	
run:
	@pipenv run python -m wxm_synthetic_data.__main__