'''
Created on Jan 19, 2014

@author: Anduril
'''
import Utils
import ChorusGlobals
from LogServer import LogServer,Level, LogType, Formatter

class ProjectConfiguration:
    '''Load options, own all project step functions'''
    
    def __init__(self, options):
        '''Provide initial full steps, input options contains basic parameters'''
        self.options=options
        self.set_output_folder()
        self.set_configfile()
        self.set_logserver()
    
    def set_output_folder(self):
        '''Set output folder
           Input: options.outputpath
           Output: self.outputdir, ChorusGlobals.outputdir'''
        self.outputdir = Utils.create_folder(self.options.outputpath, "Output", True)
        ChorusGlobals.set_outputdir(self.outputdir)
        print "Set output directory to %s" % self.outputdir
        
    def set_configfile(self):
        configfile = ConfigFile(self.options.configfile,self.options.configpath)
        self.config = configfile.config
        self.suiteinfo = configfile.suiteinfo
        ChorusGlobals.set_configfile(self.config)
        ChorusGlobals.set_suiteinfo(self.suiteinfo)

    def set_logserver(self, name = LogType.ChorusCore, level=Level.debug,
                formatter=Formatter.Console, colorconsole = False):
        self.logserver=LogServer(name, level, formatter, colorconsole)
        ChorusGlobals.set_logger(self.logserver.get_logger())
        
#     def close_logserver(self):
#         self.logserver.close_logger()

class ConfigFile:
    '''Read Config file'''
    config={}
    def __init__(self, config_filename, config_filepath=None):
        if config_filepath=="":
            config_filepath = "Config"
        else:
            config_filepath = "/".join("Config","config_file_path")
        self.cfg=Utils.read_config(config_filename, config_filepath)
        try:
            self.get_suiteinfo()
            self.get_parameters()
        except Exception,e:
            print e
            raise Exception("Cannot get suite information from config file %s" % config_filename)
        
    def get_suiteinfo(self):
        section = "CONFIG"
        tmpdict = {}
        for option in self.cfg.options(section):
            tmpdict[option] = self.cfg.get(section, option)
        self.suiteinfo = tmpdict
        
    def get_parameters(self):
        for section in self.cfg.sections():
            if section!="CONFIG":
                tmpdict = {}
                for option in self.cfg.options(section):
                    tmpdict[option] = self.cfg.get(section, option)
                self.config[section] = tmpdict