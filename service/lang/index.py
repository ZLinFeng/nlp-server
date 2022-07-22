# coding=utf-8
"""
@file    index
@date    2022/7/21 8:55 PM
@author  zlf
"""
import os.path

from service.lang.classifier import BayesClassifier
from service.service import Service
from config.settings import global_settings
from loguru import logger
import fasttext
from joblib import load

fasttext_path = os.path.join(global_settings.MODELS_HOME, "lang/fasttext.bin")
latin_lang_path = os.path.join(global_settings.MODELS_HOME, "lang/latin_lang.bin")
arab_lang_path = os.path.join(global_settings.MODELS_HOME, "lang/arab_lang.bin")
russia_lang_path = os.path.join(global_settings.MODELS_HOME, "lang/russia_lang.bin")
classifier_path = os.path.join(global_settings.MODELS_HOME, "lang/classifier.bin")


class AppService(Service):

    def __init__(self) -> None:
        super().__init__()
        self._fasttext = None  # fasttext 提供的语言检测模型
        self._latin_classifier = None  # 系统提供拉丁语的语言检测模型
        self._arab_classifier = None  # 系统提供的阿拉伯语的语言检测模型
        self._russia_classifier = None  # 系统提供的俄语的语言检测模型
        self._classifier = None  # 决策模型

    def init(self) -> None:
        # 检查模型并加载

        if not os.path.exists(fasttext_path):
            logger.exception("Missing fasttext language model.")
        self._fasttext = fasttext.load_model(fasttext_path)

        if not os.path.exists(latin_lang_path):
            logger.exception("Missing language model.")
        self._latin_classifier = BayesClassifier(latin_lang_path)

        if not os.path.exists(arab_lang_path):
            logger.exception("Missing language model.")
        self._arab_classifier = BayesClassifier(arab_lang_path)

        if not os.path.exists(russia_lang_path):
            logger.exception("Missing language model.")
        self._russia_classifier = BayesClassifier(russia_lang_path)

        if not os.path.exists(classifier_path):
            logger.exception("Missing classifier model.")
        self._classifier = load(classifier_path)

    def invoke(self, **kwargs) -> dict:
        content = kwargs["content"]
        return {"lang": "en"}
