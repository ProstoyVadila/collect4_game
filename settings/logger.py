import sys
from loguru import logger

logger.remove()
# logger.add(sys.stderr, format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}")
logger.add(sys.stderr, format="{message}")

__all__ = ["logger"]
