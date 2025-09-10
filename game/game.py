
from settings.config import Config
from game.board import Board
from settings.logger import logger

class Game:
    def __init__(self, config: Config):
        self.config = config
        self.board = Board(config.rows, config.cols)
        self.cur_idx = 0

    @property
    def cur_player_num(self) -> int:
        return self.cur_idx + 1

    @property
    def cur_symbol(self) -> str:
        return self.config.players[self.cur_idx]

    def next_player(self):
        self.cur_idx = (self.cur_idx + 1) % len(self.config.players)

    def prompt_move(self) -> int | None:
        """Returns column index (0..cols-1) or None to exit."""
        raw = input(f"{self.cur_symbol}> ").strip().lower()
        if raw in {"q", "quit", "exit"}:
            return None
        # Allow spaces/minor mistakes: "  3 "
        try:
            col = int(raw) - 1
        except ValueError:
            logger.warning("✗ Enter column number (1..{0}).".format(self.config.cols))
            return self.prompt_move()
        if not (0 <= col < self.config.cols):
            logger.warning(f"✗ Column range: 1..{self.config.cols}.")
            return self.prompt_move()
        if self.board.grid[0][col] != 0:
            logger.warning("✗ Column is full. Available:", ", ".join(str(i+1) for i in self.board.available_cols()))
            return self.prompt_move()
        return col

    def loop(self):
        logger.info(f"Connect-{self.config.connect} on {self.config.rows}x{self.config.cols}. Players: "
              + ", ".join(self.config.players))
        logger.info("(q - quit)\n")
        logger.info(self.board.render(self.config.players))

        while True:
            col = self.prompt_move()
            if col is None:
                logger.info("Game over.")
                return

            row = self.board.drop(col, self.cur_player_num)
            if row is None:
                logger.warning("✗ Move not accepted, try another column.")
                continue

            logger.info(self.board.render(self.config.players))

            if self.board.is_winner(row, col, self.cur_player_num, self.config.connect):
                logger.success(f"✓ Player {self.cur_symbol} wins!")
                return
            if self.board.is_draw():
                logger.info("= Draw.")
                return

            self.next_player()
