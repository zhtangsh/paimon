import logging
import os


def logging_config():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)s %(levelname)-8s %(message)s'
    )


def get_env(key, default_val):
    val = os.getenv(key)
    if val is None:
        return default_val
    return val
