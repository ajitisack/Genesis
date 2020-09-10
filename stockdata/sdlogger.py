import logging
from logging import FileHandler
from logging import Formatter

class SDLogger():

    @property
    def msglogger(self):
        name = f"{self.__class__.__name__}"
        msglogger = logging.getLogger(name)
        msglogger.setLevel(logging.DEBUG)
        msglogger.propagate = False
        msglogger_filehandler = FileHandler(self.logfile)
        msglogger_filehandler.setFormatter(Formatter("%(asctime)s : %(levelname)s : %(message)s", datefmt='%d-%b-%Y %H:%M:%S'))
        if len(msglogger.handlers) == 0: msglogger.addHandler(msglogger_filehandler)
        return msglogger
