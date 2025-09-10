# Collect4 game

A simple CLI game of collect 4

## Quick start

1. Clone the repository

   ```bash
   https://github.com/ProstoyVadila/collect4_game
   ```

2. Run with uv (you can install it with `pip install uv`)

   ```bash
   make run
   ```

   or with python directly (activate your virtual environment first)

   ```bash
    pip install -r requirements.txt
    python main.py
   ```

## Command-line arguments

You can override the default game settings using the following command-line arguments:

- `--rows`: number of rows (>=4)
- `--cols`: number of columns (>=4)
- `--connect`: how many in a row to win (>=2)
- `--players`: player symbols, comma-separated, e.g. "X,O,A"

Example:

```bash
python main.py --rows 8 --cols 8 --connect 5
```
