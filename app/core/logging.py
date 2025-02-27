# app/core/logging.py
import logging


def setup_logger():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    return logger


logger = setup_logger()