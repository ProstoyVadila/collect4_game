from settings.logger import logger

class Board:
    def __init__(self, rows: int, cols: int):
        self.rows= rows
        self.cols = cols
        self.grid: list[list[int]] = [[0] * cols for _ in range(rows)]
        self.last_move: tuple[int, int] | None = None  # (r, c)

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def available_cols(self) -> list[int]:
        """Columns that still have space (indexed 0..cols-1)."""
        return [c for c in range(self.cols) if self.grid[0][c] == 0]

    def drop(self, col: int, player: int) -> int | None:
        """Drop a token (gravity). Returns row or None if the column is full/out of range."""
        if not (0 <= col < self.cols) or self.grid[0][col] != 0:
            return None
        for r in range(self.rows - 1, -1, -1):
            if self.grid[r][col] == 0:
                self.grid[r][col] = player
                self.last_move = (r, col)
                return r
        return None

    def render(self, players: list[str] | str) -> str:
        if isinstance(players, str):
            logger.error("Internal error: players should be a list.")
        # Header with column numbers
        header = "   " + " ".join(f"{i:>2}" for i in range(1, self.cols + 1))
        lines = [header]
        # Board body
        for r in range(self.rows):
            row_cells = []
            for c in range(self.cols):
                v = self.grid[r][c]
                if v == 0:
                    cell = " ."
                else:
                    sym = players[v - 1]
                    cell = f"{sym:>2}"
                # Highlight the last token with brackets
                if self.last_move == (r, c):
                    cell = f"[{cell.strip():>2}]"
                row_cells.append(cell if cell.startswith("[") else f" {cell}")
            lines.append(" |" + "".join(row_cells))
        return "\n".join(lines) + "\n"

    def _count_dir(self, r: int, c: int, dr: int, dc: int, player: int) -> int:
        cnt = 0
        rr, cc = r + dr, c + dc
        while self.in_bounds(rr, cc) and self.grid[rr][cc] == player:
            cnt += 1
            rr += dr
            cc += dc
        return cnt

    def is_winner(self, r: int, c: int, player: int, need: int) -> bool:
        """Check for 4/5/... in a row for the last move."""
        for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
            total = 1 + self._count_dir(r, c, dr, dc, player) + self._count_dir(r, c, -dr, -dc, player)
            if total >= need:
                return True
        return False

    def is_draw(self) -> bool:
        return all(self.grid[0][c] != 0 for c in range(self.cols))