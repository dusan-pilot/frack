LOG_TO_FILE = {
    'version': 1,
    'formatters': {'simple': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'file': {
        'class': 'logging.handlers.RotatingFileHandler',
        'formatter': 'simple',
        'filename': 'frack.log',
        'maxBytes': 10485760,
        'backupCount': 20,
        'encoding': 'utf8'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
}

LOG_TO_CONSOLE = {
    'version': 1,
    'formatters': {'simple': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'simple'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}
