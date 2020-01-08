# -*- coding: utf-8 -*-

import logging
import logging.handlers
import os

# from .covers import CoverZip
# from .ftp import IngramFTP

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create logging format
msg_fmt = "[%(levelname)s] [%(asctime)s] [%(name)s] %(message)s"
date_fmt = "%Y-%m-%d %I:%M:%S %p"
formatter = logging.Formatter(msg_fmt, date_fmt)

# Create file handler
logfile = os.path.expanduser("~/finderscope/logs/ingram-data-services.log")
if not os.path.exists(os.path.dirname(logfile)):
    os.makedirs(os.path.dirname(logfile))
fh = logging.handlers.RotatingFileHandler(logfile, maxBytes=10485760, backupCount=5)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

# Create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

# Add logging handlers
# logger.addHandler(fh)
logger.addHandler(ch)
