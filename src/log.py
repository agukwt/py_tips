"""
Copyright (c) 2017 Pavan Ramchandani

Released under the MIT license
https://github.com/PacktPublishing/Software-Architecture-with-Python/blob/master/LICENSE
"""
# https://github.com/PacktPublishing/Software-Architecture-with-Python/blob/master/Chapter10/custom_logger.py

import logging
import logging.handlers
import time
from functools import partial


class LoggerWrapper(object):
    """ A wrapper class for logger objects with
    calculation of time spent in each step """

    def __init__(self, app_name, filename=None, level=logging.INFO, console=False):
        self.log = logging.getLogger(app_name)
        self.log.setLevel(level)

        # Add handlers
        if console:
            self.log.addHandler(logging.StreamHandler())

        if filename != None:
            self.log.addHandler(logging.FileHandler(filename))

        # Set formatting
        for handle in self.log.handlers:
            formatter = logging.Formatter('%(asctime)s [%(timespent)s]: %(levelname)-8s - %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S')
            handle.setFormatter(formatter)

        for name in ('debug', 'info', 'warning', 'error', 'critical'):
            # Creating convenient wrappers by using functools
            func = partial(self._dolog, name)
            # Set on this class as methods
            setattr(self, name, func)

        # Mark timestamp
        self._markt = time.time()

    def _calc_time(self):
        """ Calculate time spent so far """

        tnow = time.time()
        tdiff = int(round(tnow - self._markt))

        hr, rem = divmod(tdiff, 3600)
        mins, sec = divmod(rem, 60)
        # Reset mark
        self._markt = tnow
        return '%.2d:%.2d:%.2d' % (hr, mins, sec)

    def _dolog(self, levelname, msg, *args, **kwargs):
        """ Generic method for logging at different levels """

        logfunc = getattr(self.log, levelname)
        return logfunc(msg, *args, extra={'timespent': self._calc_time()})


if __name__ == "__main__":
    log = LoggerWrapper('myapp', filename='myapp.log', console=True)
    log.info("Starting application...")
    log.info("Initializing objects.")
    time.sleep(4)
    log.info("Initialization complete.")
    log.info("Loading configuration and data ...")
    time.sleep(10)
    log.info('Loading complete. Listening for connections ...')

