import logging


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logging.basicConfig(level=logging.INFO)
    handler = logging.FileHandler('syp_bot.log')
    handler.setFormatter(
        logging.Formatter(
            '[%(asctime)s][%(levelname)s] %(message)s',
            '%Y-%m-%d %H:%M:%S',
        )
    )
    logger.addHandler(handler)

    return logger
