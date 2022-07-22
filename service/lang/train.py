# coding=utf-8
"""
@file    train
@date    2022/7/22 3:28 PM
@author  zlf
"""
from service.lang.classifier import BayesClassifier
from service.lang import index

if __name__ == '__main__':
    latin_classifier = BayesClassifier(index.latin_lang_path)
    arab_classifier = BayesClassifier(index.arab_lang_path)
    russia_classifier = BayesClassifier(index.russia_lang_path)
    latin_classifier.train("/Volumes/Extend/corpus/lang/total/latin")
    arab_classifier.train("/Volumes/Extend/corpus/lang/total/arabic")
    russia_classifier.train("/Volumes/Extend/corpus/lang/total/russia")
