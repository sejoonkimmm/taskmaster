import logging

class LogColrs:
    RESET = '\033[0m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    BLUE = '\033[1;34m'
    INFO = BLUE
    ERROR = RED
    DEBUG = GREEN

class CustomFormatter(logging.Formatter):
    format_dict = {
        logging.DEBUG: LogColrs.DEBUG + '%(asctime)s - %(levelname)s - %(message)s' + LogColrs.RESET,
        logging.INFO: LogColrs.INFO + '%(asctime)s - %(levelname)s - %(message)s' + LogColrs.RESET,
        logging.ERROR: LogColrs.ERROR + '%(asctime)s - %(levelname)s - %(message)s' + LogColrs.RESET,
    }

    def format(self, record):
        log_fmt = self.format_dict.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def setup_logging():
    hanlder = logging.StreamHandler()
    hanlder.setFormatter(CustomFormatter())
    logging.basicConfig(level=logging.INFO, handlers=[hanlder])

setup_logging()