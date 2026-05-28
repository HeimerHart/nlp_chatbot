import logging
import sys

#getting logger
logger=logging.getLogger()

#create formatter

formatter= logging.Formatter(
    fmt=" %(asctime)s - %(levelname)s - %(message)s"
    )

# create handlers

stream_handler=logging.StreamHandler(sys.stdout)
file_handler=logging.FileHandler('app.log')

# set formatters
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add handler to logger
logger.handlers = [stream_handler, file_handler]

#set log level
logger.setLevel(logging.INFO)