APP_MAIN=main.py
UV=uv


.PHONY: run tests lint lint-fix

run:
	PYTHONPATH=. $(UV) run python $(APP_MAIN)

tests:
	PYTHONPATH=. $(UV) run pytest tests -v --tb=short

lint:
	@$(UV) run ruff check .

lint-fix:
	@$(UV) run ruff check --fix .
