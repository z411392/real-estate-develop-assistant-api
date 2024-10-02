from time import time
from os import getenv
from logging import getLogger, StreamHandler, DEBUG


def createLogger(name: str):
    logger = getLogger(name)
    logger.setLevel(DEBUG)
    logger.addHandler(StreamHandler())
    return logger


def createElapsedTimeProfiler():
    lastTime = time()

    def measureElapsedTime():
        nonlocal lastTime
        currentTime = time()
        elapsedTime = round(currentTime - lastTime, 2)
        lastTime = currentTime
        return elapsedTime
    return measureElapsedTime


def onDevelopment():
    return getenv("ENV") == "development"
