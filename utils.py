import logging
from datetime import datetime

def timer():
    return datetime.now().time()

def logg(msg):
    logging.basicConfig(level=logging.INFO, filename="miner.log",
                        format='%(asctime)s %(message)s')
    logging.info(msg)