from time import time
from os import getenv
from logging import getLogger, StreamHandler, INFO, Formatter


def createLogger(name: str):
    logger = getLogger(name)
    logger.setLevel(INFO)
    if not logger.handlers:
        logger.propagate = 0
        console = StreamHandler()
        formatter = Formatter('[%(name)s] %(message)s')
        console.setFormatter(formatter)
        logger.addHandler(console)
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
