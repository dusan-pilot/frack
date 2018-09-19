from logging.config import dictConfig
from logging_config import LOG_TO_CONSOLE, LOG_TO_FILE


def configure_logging(log_to_file):
    dictConfig(LOG_TO_FILE if log_to_file else LOG_TO_CONSOLE)
