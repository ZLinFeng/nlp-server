# coding=utf-8
"""
@file    index
@date    2022/7/21 8:55 PM
@author  zlf
"""
import os.path

from service.service import Service
from config.settings import global_settings
from loguru import logger
import fasttext
from joblib import load


class AppService(Service):

    def __init__(self) -> None:
        super().__init__()
        self._fasttext = None  # fasttext 提供的语言检测模型
        self._bayes_model = None  # 系统提供的语言检测模型
        self._vectorizer = None  # tf-idf的向量模型
        self._classifier = None  # 决策模型

    def init(self) -> None:
        # 检查模型并加载
        fasttext_path = os.path.join(global_settings.MODELS_HOME, "lang/fasttext.bin")
        if not os.path.exists(fasttext_path):
            logger.exception("Missing fasttext language model.")
        self._fasttext = fasttext.load_model(fasttext_path)
        lang_path = os.path.join(global_settings.MODELS_HOME, "lang/lang.bin")
        if not os.path.exists(lang_path):
            logger.exception("Missing language model.")
        self._bayes_model, self._vectorizer = load(lang_path)
        classifier_path = os.path.join(global_settings.MODELS_HOME, "lang/classifier.bin")
        if not os.path.exists(classifier_path):
            logger.exception("Missing classifier model.")
        self._classifier = load(classifier_path)

    def invoke(self, **kwargs) -> dict:
        content = kwargs["content"]
        return {"lang": "en"}
