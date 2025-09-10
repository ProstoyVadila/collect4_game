import argparse
from typing import Union
from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Settings from ENV / .env, with safe validation."""
    rows: int = 6
    cols: int = 7
    connect: int = 4
    players: Union[list[str], str] = ["X", "O"]  # player symbols

    model_config = SettingsConfigDict(
        env_prefix="GAME_",
        env_file=".env",
        case_sensitive=False,
    )

    @field_validator("players", mode="before")
    @classmethod
    def _parse_players(cls, v):
        if isinstance(v, str):
            return [p.strip() for p in v.split(",") if p.strip()]
        return v

    @model_validator(mode="after")
    def _validate_all(self):
        if self.rows < 4 or self.cols < 4:
            raise ValueError("rows/cols must be >= 4.")
        if not (2 <= self.connect <= max(self.rows, self.cols)):
            raise ValueError("connect must be between 2 and max(rows, cols).")
        if len(self.players) < 2:
            raise ValueError("At least two players are required.")
        # Normalize symbols (1-2 characters)
        self.players = [p[:2] for p in self.players]
        return self


def parse_cli_overrides() -> dict:
    """Optional CLI overrides on top of .env/ENV."""
    p = argparse.ArgumentParser(description="Console Connect-N (hotseat) with Pydantic Settings.")
    p.add_argument("--rows", type=int, help="number of rows (>=4)")
    p.add_argument("--cols", type=int, help="number of columns (>=4)")
    p.add_argument("--connect", type=int, help="how many in a row to win (>=2)")
    p.add_argument("--players", type=str, help='player symbols, comma-separated, e.g. "X,O,A"')
    args = p.parse_args()

    overrides = {}
    if args.rows is not None:
        overrides["rows"] = args.rows
    if args.cols is not None:
        overrides["cols"] = args.cols
    if args.connect is not None:
        overrides["connect"] = args.connect
    if args.players:
        overrides["players"] = args.players
    return overrides


def load_config() -> Config:
    config_base = Config()
    config_override = parse_cli_overrides()
    return Config(**(config_base.model_dump() | config_override))