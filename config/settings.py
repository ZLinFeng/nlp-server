# coding=utf-8
"""
@file    settings
@date    2022/7/21 8:21 PM
@author  zlf
"""
import os.path
import sys

from pydantic import BaseSettings
from loguru import logger


class Settings(BaseSettings):

    def __init__(self):
        super().__init__()

    HOME = os.path.dirname(os.path.dirname(__file__))
    MODELS_HOME = os.path.join(HOME, "models")

    APP_PORT = 18765
    APP_WORKERS = 3
    APP_NAME = "Nlp Server"


global_settings = Settings()
logger.add(sys.stdin, format="{time} {level} {message}", level="DEBUG")

