import logging

logging.basicConfig(filename='taskmaster.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_logging(message, level=logging.INFO):
    logging.log(level, message)