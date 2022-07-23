# coding=utf-8
"""
@file    train
@date    2022/7/22 3:28 PM
@author  zlf
"""
from service.lang.classifier import BayesClassifier

if __name__ == '__main__':
    latin_classifier = BayesClassifier()
    arab_classifier = BayesClassifier()
    russia_classifier = BayesClassifier()
    latin_classifier.train("/Volumes/Extend/corpus/lang/total/latin")
    arab_classifier.train("/Volumes/Extend/corpus/lang/total/arabic")
    russia_classifier.train("/Volumes/Extend/corpus/lang/total/russia")
