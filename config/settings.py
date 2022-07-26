# coding=utf-8
"""
@file    settings
@date    2022/7/21 8:21 PM
@author  zlf
"""
import os.path

from pydantic import BaseSettings


class Settings(BaseSettings):

    def __init__(self):
        super().__init__()

    APP_HOME = os.path.dirname(os.path.dirname(__file__))
    MODELS_HOME = os.path.join(APP_HOME, "models")

    APP_PORT = 18765
    APP_WORKERS = 1
    APP_NAME = "Nlp Server"


global_settings = Settings()
