# coding=utf-8
"""
@file    context
@date    2022/7/23 6:57 PM
@author  zlf
"""
import os

from config.settings import global_settings


class ApplicationContext:
    pass


def scan_modules(module_list: list[str]):
    """
    针对不引用的文件进行
    手动的import  module
    :param module_list: 要加载的module的列表  目前只加载一层
    """
    for module_str in module_list:
        module_path = os.path.join(global_settings.APP_HOME, module_str.replace(".", "/"))
        files = [filename for filename in os.listdir(module_path) if
                 not filename.startswith("__") and filename.endswith(".py")]
        for py_file in files:
            module_name = module_str + "." + py_file[:-3]
            __import__(module_name)
