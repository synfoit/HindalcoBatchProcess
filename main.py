import logging, os
from SerialDataReader import SerialDataReader
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

ports = os.getenv('PORTS')
ports = ports.split(',')

logLevel = os.getenv('LOG_LEVEL')
logLevel = 40 if logLevel is None else int(logLevel)

logger = logging.getLogger('app_logger')
handler = RotatingFileHandler(filename='logs/hindalco_log.log',
                              maxBytes=1024 * 1024 * 20,
                              backupCount=10)
handler.setFormatter(logging.Formatter(
    fmt='%(asctime)s %(levelname)s %(threadName)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

logger.addHandler(handler)
logger.setLevel(logLevel)

if __name__ == '__main__':
    logger.info(f'Starting batch process on {len(ports)} ports')
    for port in ports:
        logger.info(f'Starting reading on port {port}')
        sd = SerialDataReader(port, port)
        sd.start()

