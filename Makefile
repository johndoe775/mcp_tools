env:
	pip install --upgrade pip && pip install uv && uv venv

install:
	uv sync

git:
	git add .
	git status
	git commit -m "recent edits"
	git push


format:
	python3 -m black . --include '\.py'

run:
	uv run main.py
