env:
	pip install --upgrade pip && pip install uv && uv venv

add:
	uv add -r requirements.txt

sync:
	uv sync && clear

git:
	git add .
	git status
	git commit -m "recent edits"
	git push
	clear


format:
	python3 -m black . --include '\.py'

lint:
	python3 -m pylint **/*.py

run:
	uv run main.py

