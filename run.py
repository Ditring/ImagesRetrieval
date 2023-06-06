import os
import pickle
from flask import Flask, render_template, request, jsonify
from common import CosSimilarity
import numpy as np
import random
from features import SURF
import joblib

app = Flask(__name__)
features = None

kmeans_model = joblib.load('./model/kmeans.m')  # 加载k-means模型

def search_top_k(k, img_name, similarity=CosSimilarity()):
    anchor = None
    global features
    surf = SURF()
    surf.set_kmeans_model(kmeans_model)
    anchor = surf.get_feature(img_name)
    index_sim = []
    for i in range(len(features)):
        index_sim.append([i, similarity.get_similarity(anchor, features[i].feature)])
    # 排序 找出top-k
    index_sim = np.array(index_sim)
    sorted_index = index_sim[:, 1].argsort()[::-1][1:k + 1]  # 排除自身
    print(sorted_index)
    result = []
    for i in sorted_index:
        result.append(features[i].img_name)
    return result


@app.route('/')
def Demo():
    return render_template('homepage.html')


@app.route('/action/upload/', methods=['POST'])
def search():
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            # 选择存储的路径
            save_path = './temp/'
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            # 保存图片文件
            image.save(os.path.join(save_path, image.filename))
            global features
            # 如果features为空证明还未加载特征库，先加载一下
            if features is None:
                if os.path.exists('./pickle/features.pkl'):
                    with open('./pickle/features.pkl', 'rb') as f:
                        features = pickle.load(f)
            result = {}
            # 如果未创建特征库则需要先创建特征库，如果已创建则返回前5个最相似的图片
            if features is None:
                result['code'] = -1
                result['message'] = '尚未建立特征库，请先运行BuildImageFeature.py文件'
            else:
                result['code'] = 1
                result['img_names'] = search_top_k(5, './temp/' + image.filename)
            return jsonify(result)


@app.route('/action/get_result/', methods=['POST'])
def get_search_result():
    img_name = request.get_json()
    img_name = img_name['img_name']
    global features
    # 如果features为空证明还未加载特征库，先加载一下
    if features is None:
        if os.path.exists('./pickle/features.pkl'):
            with open('./pickle/features.pkl', 'rb') as f:
                features = pickle.load(f)
    result = {}
    # 如果未创建特征库则需要先创建特征库，如果已创建则返回前5个最相似的图片
    if features is None:
        result['code'] = -1
        result['message'] = '尚未建立特征库，请先运行BuildImageFeature.py文件'
    else:
        result['code'] = 1
        result['img_names'] = search_top_k(5, img_name)
    return jsonify(result)

