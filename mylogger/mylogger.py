""" Use the follofing to use this logger:
log = mylogger.Logger(level='INFO')
If you'd like to set/change Splunk Modular Input in log message:
log.source = splunk_input_name
If you'd like to dynamically change logging level:
log.setLevel(input_item['log_level'])
"""


import logging
import os
import inspect
import time


if 'SPLUNK_HOME' in os.environ:
    SPLUNK_HOME_DIR = os.path.expandvars('$SPLUNK_HOME')
    log_subdirs = ['var', 'log']
    log_dir = os.path.join(SPLUNK_HOME_DIR)
    for log_subdir in log_subdirs:
        log_dir = os.path.join(log_dir, log_subdir)
    LOG_DIR = log_dir
elif os.path.exists(os.path.expandvars('/tmp')):
    LOG_DIR = os.path.expandvars('/tmp')
else:
    log_dir = os.path.dirname(os.path.abspath(inspect.stack()[1][1]))
    LOG_DIR = os.path.expandvars(log_dir)
LOG_FORMAT = 'timestamp="%(asctime)s" log_level="%(levelname)s" %(message)s'
DEFAULT_LOG_LEVEL = logging.INFO
LOGGER = None


class Logger():
    """ custom logger for Splunk """

    def __init__(self, level=DEFAULT_LOG_LEVEL, source=None):
        self.log_name = os.path.splitext(os.path.basename(inspect.stack()[1][1]))[0]
        self.log_file_path = os.path.join(LOG_DIR, self.log_name) + '.log'
        self.log_level = level
        self.source = source
        self.component = None
        self.log = self._get_logger()

    def _get_logger(self):
        logger = logging.getLogger(self.log_name)
        handler = logging.FileHandler(
            '{}/{}.log'.format(LOG_DIR, self.log_name))
        formatter = logging.Formatter(LOG_FORMAT)
        logging.Formatter.converter = time.gmtime
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(self.log_level)
        return logger

    def setLevel(self, level):
        """ dynamically re-set logging level """
        self.log.setLevel(level)

    def _gen_message(self, message):
        """ generate final message """
        if self.component is None:
            component = str(inspect.stack()[2][3])
        else:
            component = self.component
        message = 'input_name="' + str(self.source) + \
                  '" function="' + str(component) + \
                  '" message="' + str(message) + '"'
        return message

    def debug(self, message=None):
        message = self._gen_message(message)
        self.log.debug(message)

    def info(self, message=None):
        message = self._gen_message(message)
        self.log.info(message)

    def warn(self, message=None):
        message = self._gen_message(message)
        self.log.warn(message)

    def error(self, message=None):
        message = self._gen_message(message)
        self.log.error(message)

    def exception(self, message=None):
        message = self._gen_message(message)
        self.log.exception(message)
