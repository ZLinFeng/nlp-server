# coding=utf-8
"""
@file    utils
@date    2022/6/28 7:44 PM
@author  zlf
"""


def app_filter(order: int):
    def wrapper(cls):
        return cls

    return wrapper


def is_empty(text: str) -> bool:
    return text is None or len(text) == 0
