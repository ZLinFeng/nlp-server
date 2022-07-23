# coding=utf-8
"""
@file    context
@date    2022/7/23 11:55 AM
@author  zlf
"""
import os

content = {}


def scan_and_register() -> None:
    service_dir = os.path.dirname(__file__)
    dirs = [dirname for dirname in os.listdir(service_dir) if os.path.isdir(dirname)]
    for name in dirs:
        print(name)


if __name__ == '__main__':
    scan_and_register()
