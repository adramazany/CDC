from configparser import ConfigParser

cfg = ConfigParser()
cfg.read("config.ini")

def get(key):
    return get("default",key)

def get(section,key):
    value = cfg.get(section,key)
    # print('config > %s > %s = %s'%(section,key,value))
    return value
