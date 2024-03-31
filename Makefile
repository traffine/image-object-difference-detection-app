SHELL := /bin/bash

# Variables definitions
# -----------------------------------------------------------------------------

ifeq ($(TIMEOUT),)
TIMEOUT := 60
endif

export POETRY=poetry run
export PYSEN=${POETRY} pysen run
export PYTEST=${POETRY} pytest

# Target section and Global definitions
# -----------------------------------------------------------------------------
.PHONY: all clean test install up down run st

test:
	PYTHONPATH=app ${PYTEST} tests -vv --show-capture=all

lint:
	${PYSEN} lint

format:
	${PYSEN} format

install: generate_dot_env
	pip install --upgrade pip
	pip install poetry
	poetry install --no-root

run:
	PYTHONPATH=app/ poetry run python app/main.py

st:
	PYTHONPATH=app/ poetry run streamlit run app/st.py

up: generate_dot_env
	docker-compose build
	docker-compose up -d

down:
	docker-compose down

generate_dot_env:
	@if [[ ! -e .env ]]; then \
		cp .env.example .env; \
	fi

clean:
	@find . -name '*.pyc' -exec rm -rf {} \;
	@find . -name '__pycache__' -exec rm -rf {} \;
	@find . -name 'Thumbs.db' -exec rm -rf {} \;
	@find . -name '*~' -exec rm -rf {} \;
	rm -rf .cache
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf htmlcov
	rm -rf .tox/
	rm -rf docs/_build
