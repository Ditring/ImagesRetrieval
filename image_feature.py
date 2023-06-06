from common import ImageFeature
from Features import SURF
import joblib
import os
import pickle
import time


def main():
    path = './static/dataset/'
    filenames = os.listdir(path)

    surf = SURF()  # 创建SURF提取器
    kmeans_model = joblib.load('./kmeans.m')  # 加载k-means模型
    surf.set_kmeans_model(kmeans_model)
    # 如果特征pkl文件存在则直接读取创建特征库，如果不存在需要先getfeature建立图片特征库
    if os.path.exists('./features.pkl'):
        with open('./features.pkl', 'rb') as f:
            features = pickle.load(f)
    else:
        features = []
        i = 0
        for f in filenames:
            feature = surf.get_feature(path + f)
            features.append(ImageFeature(f, feature))  # 创建ImageFeature实例并将文件名和特征向量存入列表
            i += 1
            if i % 10 == 0:
                print('{} 进度：{}/{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), i,
                                           len(filenames)))

        with open('./features.pkl', 'wb') as f:  # 特征向量列表存文件
            pickle.dump(features, f)
    print('{} 特征库已建立，共{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                    len(features)))


if __name__ == '__main__':
    main()
