.PHONY: all fixtures static locale

all: test clean lint

test:
	mkdir -p reports; touch reports/coverage.xml; chmod -R 777 reports
	pytest ${APP}
	chmod -R 777 reports

lint:
	mkdir -p reports
	touch reports/bandit.json;
	touch reports/pylint.txt;
	chmod -R 777 reports/
	flake8
	isort -c --recursive
	bandit -s B101 -r -f json -o reports/bandit.json jobadvisor
	pylint jobadvisor | tee reports/pylint.txt
	chmod -R 777 reports

static:
	python3 manage.py collectstatic --noinput

fixtures:
	python3 manage.py loaddata fixtures/auth.json
	python3 manage.py loaddata fixtures/category.json
	python3 manage.py loaddata fixtures/question.json
	python3 manage.py loaddata fixtures/variant.json

test-data:
	python3 manage.py loaddata fixtures/tests.json

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

locale:
	python3 manage.py makemessages --all
	python3 manage.py compilemessages

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	isort -y --recursive