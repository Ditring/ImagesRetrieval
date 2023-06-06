import cv2
from abc import ABCMeta, abstractmethod
import numpy as np


class AbstractFeature(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_feature(self, img, bboxes):
        pass


class SURF(AbstractFeature):
    # 初始化SURF特征提取器
    def __init__(self, cluster_center=500):
        self.surf = cv2.xfeatures2d.SURF_create(
            hessianThreshold=3000
            , nOctaves=4
            , nOctaveLayers=3
            , extended=True
            , upright=False
        )
        self.cluster_center = cluster_center

    # 从图像中提取SURF特征
    def get_surf(self, filename, box=None):
        img = cv2.imread(filename)  # 读取文件
        if box is not None:
            img = img[box[1]:box[3], box[0]:box[2], :]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转化为灰度图
        keyPoint, descriptor = self.surf.detectAndCompute(img, None)  # 特征提取得到关键点以及对应的描述符（特征向量）
        return img, keyPoint, descriptor

    # 设置K-Means聚类模型
    def set_kmeans_model(self, kmeans):
        self.kmeans = kmeans

    # 获取图像中标注框内特征向量
    def get_feature(self, img, bboxes=None):
        if self.kmeans is None:
            raise ValueError('请先对self.kmeans 赋值')
        img, keyPoint, descriptor = self.get_surf(img, bboxes)
        feature = np.zeros(self.cluster_center, dtype=np.float)
        if descriptor is not None:
            cluster_classify = self.kmeans.predict(descriptor)
            for i in range(len(cluster_classify)):
                score = self.kmeans.score(np.reshape(descriptor[i], (1, -1)))
                feature[int(cluster_classify[i])] += np.abs(score)
        return feature
