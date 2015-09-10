#coding:utf-8
import logging

def InitLog(LOGPATH):
    ##################user config ##################
    logger = logging.getLogger(LOGPATH)
    #############################################
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOGPATH)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
logger = InitLog("network-server")
logger.error("create socket failed")
