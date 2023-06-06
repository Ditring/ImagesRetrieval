import os
import time
from Features import SURF
from sklearn.cluster import KMeans
import joblib
import pickle
import random


# 创建样本中心
def build_sample_center(paths, centers=500):
    # 检查路径是否为元组或者是列表，不是则转换为列表
    if not isinstance(paths, (tuple, list)):
        paths = [paths]
    all_file_path = []  # 存储所有图片的文件路径
    for p in paths:
        filenames = os.listdir(p)  # 获取文件夹中的所有文件名
        all_file_path.extend([p + f for f in filenames])
    random.shuffle(all_file_path)
    # all_file_path = all_file_path[:500] # 可选，限制处理的图片数量
    print('{} 共计图片数目:{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), len(all_file_path)))
    if os.path.exists('./descriptor.pkl'):
        with open('./descriptor.pkl', 'rb') as f:
            descriptor = pickle.load(f)
    else:
        descriptor = get_surf_descriptor(all_file_path)
        with open('./descriptor.pkl', 'wb') as f:
            pickle.dump(descriptor, f)
    # 打乱特征点描述符descriptor列表的顺序，并选择其中的前10%作为样本
    random.shuffle(descriptor)
    descriptor = descriptor[:int(len(descriptor) / 10)]
    print('{} 共计特征点描述:{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), len(descriptor)))
    # 如果之前已经创建kmeans模型了则加载即可，否则需要创建
    if os.path.exists('./kmeans.m'):
        kmeans = joblib.load('./kmeans.m')
        print('loaded {}'.format('./kmeans.m'))
        param = {'max_iter': 2}
        kmeans = kmeans.set_params(**param)
    else:
        kmeans = KMeans(n_clusters=centers
                        , precompute_distances=True
                        , max_iter=1
                        , n_jobs=-1
                        )
    kmeans.fit(descriptor)
    print(kmeans.get_params())
    # 要获得预测向量属于哪个类别/要获得与类别中心的距离
    print('{} kmeans聚类模型创建完毕'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    # 保存模型
    joblib.dump(kmeans, './kmeans.m'.format(centers))


# 获取图片的SURF特征点描述
def get_surf_descriptor(filenames):
    surf = SURF()
    result = []
    for f in filenames:
        img, keypoint, d = surf.get_surf(f)
        if d is not None:
            result.extend(d)
    return result


if __name__ == '__main__':
    paths = ['D:/Projects/PythonProject/ImagesRetrieval/static/dataset/']  # 此处应当输入你配置的数据集的地址，如果地址不是这个记得全局修改一下地址信息
    build_sample_center(paths)
