import logging

def setup_logging():
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )