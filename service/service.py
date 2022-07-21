# coding=utf-8
"""
@file    service
@date    2022/7/21 8:51 PM
@author  zlf
"""
import abc


class Service(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def invoke(self, **kwargs):
        pass
