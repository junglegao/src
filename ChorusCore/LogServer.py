'''
Created on Jan 16, 2012

@author: Mingze, Anduril
'''
import logging, os

class Name:
    ChorusCore = "ChorusCore"
    Script = "Script"
    MockServer = "MockServer"
    Request = "Request"
    Response = "Response"

class Formatter:
    Console = "%(message)s"
    ChorusCore = "%(asctime)s - %(name)s - {%(pathname)s:%(lineno)d} - %(levelname)s - %(message)s"
    Script = "%(asctime)s - %(levelname)s - %(message)s - {%pathname)s:%(lineno)d}"
    MockServer = "%(asctime)s - %(name)s - {%(pathname)s:%(lineno)d} - %(levelname)s - %(message)s"
    Request = "%(url)s \n\t%(method)s \n\t%(headers)s \n\t%(body)s"
    Response = "%(url)s \n\t%(status)s \n\t%(headers)s \n\t%(body)s"
    
class Level:
    notset = logging.NOTSET
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR
    critical = logging.CRITICAL

class LogServer:
    filehandler=[]
    def __init__(self,name=Name.ChorusCore,level=Level.debug,
                formatter=Formatter.Console):
        rootlogger = logging.getLogger()
        rootlogger.setLevel(Level.notset)
        self.logger=logging.getLogger(name)
        self.logger.setLevel(Level.notset)
        self.add_consolehandler(level, formatter)
    
    def get_logger(self):
        return self.logger
    
    def add_consolehandler(self,level=Level.debug,
                    formatter=Formatter.ChorusCore):
        self.consolehandler=logging.StreamHandler()
        self.consolehandler.setFormatter(logging.Formatter(formatter))
        self.consolehandler.setLevel(level)
        self.logger.addHandler(self.consolehandler)
    
    def add_filehandler(self,level=Level.debug,
                    formatter=Formatter.ChorusCore,
                    filepath=None,filename=None):
        if filename is None or filepath is None:
            raise Exception("Invalid Log file path %s and name %s" % (filepath,filename))
        logfile = os.path.join( filepath, filename)
        handler=logging.FileHandler(logfile)
        handler.setFormatter(logging.Formatter(formatter))
        handler.setLevel(level)
        self.logger.addHandler(handler)
        self.filehandler.append(handler)
    
    def close_logger(self):
        self.consolehandler.flush()
        self.logger.removeHandler(self.consolehandler)
        self.consolehandler.close()
        for handler in self.filehandler:
            handler.flush()
            self.logger.removeHandler(handler)
            handler.close()
