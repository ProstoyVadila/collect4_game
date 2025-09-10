from settings.config import load_config
from game.game import Game
from settings.logger import logger

def main():
    try:
        config = load_config()
        Game(config).loop()
    except KeyboardInterrupt:
        logger.info("\nExit.")
    except EOFError:
        logger.error("\nGot error.")


if __name__ == "__main__":
    main()