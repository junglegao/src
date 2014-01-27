'''
Created on Jan 19, 2014

@author: Anduril
'''
def set_outputdir(path):
    '''Mark output folder as global'''
    global outputdir
    outputdir = path
    
def get_outputdir():
    '''Return output folder'''
    return outputdir
        
def set_configfile(configfile):
    '''Mark configfile as global'''
    global config
    config = configfile
    
def get_configfile():
    '''Return config file'''
    return config

def set_logger(loggerobj):
    '''Mark logger as global'''
    global logger
    logger=loggerobj
    
def get_logger():
    '''Return logger'''
    return logger