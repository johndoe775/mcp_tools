env:
	pip install --upgrade pip && pip install uv && uv venv

sync:
	uv sync

git:
	git add .
	git status
	git commit -m "recent edits"
	git push
	clear


format:
	python3 -m black . --include '\.py'

run:
	uv run main.py
