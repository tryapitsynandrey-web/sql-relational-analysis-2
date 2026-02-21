.PHONY: install run test export docs

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

run:
	.venv/bin/python start_analysis.py

test:
	.venv/bin/pytest tests/

export:
	.venv/bin/python scripts/generate_report.py

docs:
	.venv/bin/python scripts/generate_docs.py
