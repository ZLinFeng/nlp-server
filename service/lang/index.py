# coding=utf-8
"""
@file    index
@date    2022/7/21 8:55 PM
@author  zlf
"""
from service.service import Service


class AppService(Service):

    def __init__(self) -> None:
        super().__init__()
        self._fasttext = None  # fasttext 提供的语言检测模型
        self._model = None  # 系统提供的语言检测模型

    def init(self):
        # 检查模型并加载
        pass

    def invoke(self, **kwargs):
        pass
