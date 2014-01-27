'''
Created on Jan 19, 2014

@author: Anduril
'''
import os, stat, shutil, errno, ConfigParser,pyclbr,copy
import datetime
def remove_path(path):
    '''Remove file or folder'''
    try:
        
        if os.path.isdir(path):
            shutil.rmtree(path, ignore_errors=False, onerror=handle_readonly)
        elif os.path.exists(path):
            os.remove(path)
        print "Remove Directory %s Successfully" % path
    except Exception,e:
        print e
        raise Exception("Cannot remove the directory %s" % path)

def handle_readonly(func, path, exc):
    '''Callable function for removing readonly access'''
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
        func(path)
    else:
        raise Exception("Cannot handle read-only file, need to remove %s manually" % path)
    
def create_folder(folderpath, foldername, refreshflag=True):
    '''create a folder: 
       refreshflag=True: if folder exists, then delete it and re-create; else just create the folder
       refreshflag=False: if folder doesn't exist, then create the folder'''
    if folderpath=="" or os.path.isdir(folderpath):
        newfolder = os.path.join(folderpath,foldername)
        if os.path.isdir(newfolder):
            if refreshflag:
                remove_path(newfolder)
                os.makedirs(newfolder)
        else:
            os.makedirs(newfolder)
    else:
        raise Exception("Invalid Folder %s" % folderpath)
    return newfolder

def get_filestr(paths = None,filename = ''):
    '''Return File Fullpath'''
    rootpath = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    fullpath = rootpath
    for path in paths:
        fullpath = os.path.join(fullpath, path)
    if not os.path.exists(fullpath):
        os.makedirs(fullpath)
    return os.path.join(fullpath,filename)

def read_config(config_filename,config_filepath):
    '''Read cfg file'''
    cfg = ConfigParser.RawConfigParser()
    print "Set config file to %s/%s" % (config_filepath,config_filename)
    paths = config_filepath.split("/")
    cfg.read(get_filestr(paths, config_filename))
    if not cfg.sections():
        raise Exception("Cannot read config info from %s at %s, please check you config filename and path!" % (config_filename,config_filepath))
    return cfg

def get_timestamp():
    '''Return currenttime in '''
    now = datetime.datetime.utcnow()
    timestamp = '%s%s%s%s%s%s%s' % (now.year,now.month,now.day,now.hour,now.minute,now.second,now.microsecond)
    return timestamp

def class_browser(modulepath):
    return pyclbr.readmodule_ex(modulepath)

def create_entity(obj):
    return copy.copy(obj)