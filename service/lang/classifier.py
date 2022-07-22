# coding=utf-8
"""
@file    classifier
@date    2022/6/27 6:27 PM
@author  zlf
"""
import abc
import os.path

import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

import utils
from loguru import logger
from joblib import dump, load


class LangCode:

    def __init__(self):
        self._lang2int = {
            "de": 1,
            "en": 2,
            "es": 3,
            "fi": 4,
            "fr": 5,
            "hu": 6,
            "id": 7,
            "it": 8,
            "lt": 9,
            "ma": 10,
            "nl": 11,
            "pl": 12,
            "pt": 13,
            "ro": 14,
            "sv": 15,
            "ar": 16,
            "ur": 17,
            "fa": 18,
            "ru": 19,
            "uk": 20
        }

    def get_lang_code(self, lang: str) -> int:
        if utils.is_empty(lang):
            return 2
        return self._lang2int[lang]

    def get_lang(self, code: int) -> str:
        for key, value in self._lang2int.items():
            if value == code:
                return key
        return "en"


lang_2_code = LangCode()


class IClassifier(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def train(self, input_path: str, re_train: bool) -> bool:
        """
        分类器训练
        :param re_train: 是否要重新训练
        :param input_path: 数据集的目录, 目录下文件名即为label, 文件内容包含了训练集和测试集
        :return: 成功 True
        """
        pass

    @abc.abstractmethod
    def predict(self, input_content: str) -> list[str]:
        """
        预测
        :param input_content: 预测的文本的输入
        :return: 预测结果
        """
        pass

    @abc.abstractmethod
    def test(self):
        """
        测试
        :return:
        """
        pass

    @staticmethod
    def load_data(filename: str) -> [list, list]:
        """
        读文件加载数据
        :param filename: 文件路径
        :return: 文本以及label
        """
        X = []
        Y = []
        with open(file=filename, mode="r", encoding="utf8") as f:
            label_str = os.path.basename(filename)
            label_code = lang_2_code.get_lang_code(label_str)
            for line in f:
                line = line.strip("\n")
                X.append(line)
                Y.append(label_code)
            return [X, Y]


class BayesClassifier(IClassifier):
    """
    贝叶斯分类器
    """

    def __init__(self, model_path: str):
        self._vectorizer = None
        self._classifier = MultinomialNB()
        self._model_name = model_path
        self._init_vectorizer()
        self._x_train = []
        self._y_train = []
        self._x_test = []
        self._y_test = []

    def train(self, input_path: str, re_train: bool = False) -> bool:
        if not re_train and os.path.exists(self._model_name):
            logger.info(f"Load exist model: {self._model_name}")
            self._classifier, self._vectorizer = load(self._model_name)
            return True

        if not os.path.exists(input_path) or os.path.isfile(input_path):
            logger.error("input_path should be a dirname.")
            return False

        labels = [label for label in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, label))]
        for label in labels:
            logger.info(f"Load corpus {label}...")
            X_train, Y_train = IClassifier.load_data(os.path.join(input_path, label))
            x_train, x_test, y_train, y_test = train_test_split(X_train, Y_train, train_size=100000)
            self._x_train.extend(x_train)
            self._y_train.extend(y_train)
            self._x_test.extend(x_test)
            self._y_test.extend(y_test)
        self._vectorizer.fit(self._x_train)
        logger.info("Finish vectorizer...")
        features = self._vectorizer.transform(self._x_train)
        self._classifier.fit(features, self._y_train)
        logger.info("Finish bayes classifier...")
        if os.path.exists(self._model_name):
            os.remove(self._model_name)
        dump((self._classifier, self._vectorizer), self._model_name)
        return True

    def predict(self, input_content: list) -> list[str]:
        code_list = self._classifier.predict(self._vectorizer.transform(input_content))
        return [lang_2_code.get_lang(code) for code in code_list]

    def test(self):
        self._classifier.score(self._vectorizer.transform(self._x_test), self._y_test)

    def _init_vectorizer(self):
        self._vectorizer = TfidfVectorizer(ngram_range=(1, 1),
                                           token_pattern="\\w+",
                                           decode_error="replace",
                                           dtype=np.float32)
