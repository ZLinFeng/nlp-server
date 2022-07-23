# coding=utf-8
"""
@file    index
@date    2022/7/21 8:55 PM
@author  zlf
"""
import os.path
import time

import utils
from service.lang.classifier import BayesClassifier
from service.lang.preprocessor import IPreprocessor, LatinPreprocessor, CJKPreprocessor, ArabPreprocessor, \
    RussiaPreprocessor
from service.service import Service
from config.settings import global_settings
from loguru import logger
import fasttext

fasttext_path = os.path.join(global_settings.MODELS_HOME, "lang/fasttext.bin")
latin_lang_path = os.path.join(global_settings.MODELS_HOME, "lang/latin_lang.bin")
arab_lang_path = os.path.join(global_settings.MODELS_HOME, "lang/arab_lang.bin")
russia_lang_path = os.path.join(global_settings.MODELS_HOME, "lang/russia_lang.bin")
classifier_path = os.path.join(global_settings.MODELS_HOME, "lang/classifier.bin")


class LangService(Service):

    def __init__(self) -> None:
        super().__init__()
        fasttext.FastText.eprint = lambda x: None
        self._fasttext = None  # fasttext 提供的语言检测模型
        self._latin_classifier = None  # 系统提供拉丁语的语言检测模型
        self._arab_classifier = None  # 系统提供的阿拉伯语的语言检测模型
        self._russia_classifier = None  # 系统提供的俄语的语言检测模型
        self._classifier = None  # 决策模型

        self._latin_preprocessor = LatinPreprocessor()
        self._cjh_preprocessor = CJKPreprocessor()
        self._arab_preprocessor = ArabPreprocessor()
        self._russia_preprocessor = RussiaPreprocessor()
        self.init()  # 未使用依赖注入之前

    def init(self) -> None:
        # 检查模型并加载

        if not os.path.exists(fasttext_path):
            logger.exception("Missing fasttext language model.")
        self._fasttext = fasttext.load_model(fasttext_path)

        if not os.path.exists(latin_lang_path):
            logger.exception("Missing language model.")
        self._latin_classifier = BayesClassifier()
        self._latin_classifier.load_model(latin_lang_path)

        if not os.path.exists(arab_lang_path):
            logger.exception("Missing language model.")
        self._arab_classifier = BayesClassifier()
        self._arab_classifier.load_model(arab_lang_path)

        if not os.path.exists(russia_lang_path):
            logger.exception("Missing language model.")
        self._russia_classifier = BayesClassifier()
        self._russia_classifier.load_model(russia_lang_path)

        """
        if not os.path.exists(classifier_path):
            logger.exception("Missing classifier model.")
        self._classifier = load(classifier_path)
        """

    def predict(self, content: str) -> str:
        content = IPreprocessor.word_filter(content)
        p_res = "o"
        if utils.is_empty(content):
            logger.info(p_res)
            return p_res
        content = content.lower()
        lang2count = {"latin": 0, "arab": 0, "o": 0, "ru": 0, "ta": 0, "th": 0, "km": 0, "ja": 0, "zh": 0}
        for char in content:
            if char in self._latin_preprocessor.latin_char or "a" <= char <= "z":
                lang2count["latin"] += 1
            elif "\u0600" <= char <= "\u06FF" \
                    or "\u0750" <= char <= "\u077F" \
                    or "\u08A0" <= char <= "\u08FF" \
                    or "\u0001\uEE00" <= char <= "\u0001\uEEFF":
                lang2count["arab"] += 1
            elif "\u0410" <= char <= "\u044F":
                lang2count["ru"] += 1
            elif "\u0B80" <= char <= "\u0BFF" or "\u0001\u1FC0" <= char <= "\u0001\u1FFF":
                lang2count["ta"] += 1
            elif "\u0E00" <= char <= "\u0E7F":
                lang2count["th"] += 1
            elif "\u1780" <= char <= "\u17FF":
                lang2count["km"] += 1
            elif "\u3040" <= char <= "\u309F" or "\u30A0" <= char <= "\u30FF" or "\u31F0" <= char <= "\u31FF":
                lang2count["ja"] += 1
            elif "\u3400" <= char <= "\u4DBF" or "\u4E00" <= char <= "\u9FFF" or "\uF900" <= char <= "\uFAFF":
                lang2count["zh"] += 1
            elif " " == char:
                continue
            else:
                lang2count["o"] += 1

        pre_predict_key = "o"
        pre_predict_count = 0
        for key, value in lang2count.items():
            if value > pre_predict_count:
                pre_predict_key = key
                pre_predict_count = value
        match pre_predict_key:
            case "latin":
                t1 = time.time()
                content = self._latin_preprocessor.apply(content)
                t2 = time.time()
                logger.info(f"预处理耗时: {t2 - t1}")
                if utils.is_empty(content):
                    p_res = "o"
                else:
                    start_time = time.time()
                    p_res = self._latin_classifier.predict([content])[0]
                    end_time = time.time()
                    logger.info(f"预测耗时: {end_time - start_time}")
            case "arab":
                content = self._arab_preprocessor.apply(content)
                if utils.is_empty(content):
                    p_res = "o"
                else:
                    p_res = self._arab_classifier.predict([content])[0]
            case "ru":
                content = self._russia_preprocessor.apply(content)
                if utils.is_empty(content):
                    p_res = "o"
                else:
                    p_res = self._russia_classifier.predict([content])[0]
            case _:
                p_res = pre_predict_key

        return p_res

    def invoke(self, **kwargs):
        if kwargs.__contains__("content"):
            return self.predict(kwargs["content"])
        else:
            return "unknown"


lang_service = LangService()
