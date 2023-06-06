import numpy as np
from abc import ABCMeta, abstractmethod


# 用于比较相似度的抽象基类
class AbstractSimilarity(object):
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def get_similarity(feature1, feature2):
        pass

class ImageFeature(object):
    def __init__(self, img_name, feature):
        self._img_name = img_name
        self._feature = feature

    @property
    def img_name(self):
        return self._img_name

    @img_name.setter
    def img_name(self, value):
        self._img_name = str(value)

    @property
    def feature(self):
        return self._feature

    @feature.setter
    def feature(self, value):
        self._feature = value


# 获取余弦相似度
class CosSimilarity(AbstractSimilarity):

    @staticmethod
    def get_similarity(f1, f2):
        if isinstance(f1, list):
            f1 = np.array(f1).reshape((-1,))
        if isinstance(f2, list):
            f2 = np.array(f2).reshape((-1,))
        return CosSimilarity.get_cos(f1, f2)

    @staticmethod
    def get_cos(vector_a, vector_b):
        vector_a = np.reshape(vector_a, (-1))
        vector_b = np.reshape(vector_b, (-1))
        num = np.dot(vector_a, vector_b.T)
        denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
        if denom == 0:
            sim = 0.0
        else:
            cos = num / denom
            sim = 0.5 + 0.5 * cos
        return sim


# # 获取欧氏距离
# class EuclideanDistance(AbstractDistance):
#     @staticmethod
#     def get_distance(feature1, feature2, flags=''):
#         distance = np.power(feature1 - feature2, 2).sum()
#         return distance
