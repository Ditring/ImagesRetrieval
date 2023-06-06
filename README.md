# ImageSearch
计算机视觉课程大作业，图像检索系统

内容列表
- [1.介绍](#1.介绍)
- [2.环境](#2.环境)
- [3.使用说明](#3.使用说明)
  - [Step1](#Step1)
  - [Step2](#Step2)
  - [Step3](#Step3)
- [4.相关文章](#4.相关文章)

该文档是为了帮助你快速了解该系统的操作流程
##1.介绍
###1.1基本技术
本系统使用K-Means聚类算法聚类，SURF算法提取图像关键点和描述符，使用Flask框架搭建web应用

后端由python实现

前端直接用静态文件写的，很简单
###1.2功能
- 可以点击选择文件按钮或者图片上传图片，搜索图像库中相似的图片
- 点击查询结果中的缩略图可以查看搜索结果的高清大图
###1.3数据集介绍
数据集是The Oxford Buildings Dataset
牛津建筑数据集包含 5062 张图像，这些图像是通过搜索特定的牛津地标从Flickr收集的。
###1.4系统主要模块
整个系统包括三个部分：输出KMeans模型，建立图片特征库，通过Flask运行web应用
##2.环境
```shell
python 3.7
opencv-python 3.4.2.16
opencv-contrib-python 3.4.2.16
scikit-learn 0.22.1
scipy 1.4.1
Flask 1.1.2
```

##3.使用说明
####Step1：
安装环境中所需依赖
####Step2：
下载数据集，The Oxford Buildings Dataset

下载完成后将数据集放到指定的文件夹中，并在代码中数据集地址进行相应的修改，默认地址为"./static/dataset/"

配置数据集路径！！！

####Step3：
运行ClusteringAnalysis.py训练K-Means模型

配置数据集路径！！！

####Step4：
运行BuildImageFeature.py建立图片特征库

配置数据集路径！！！

####Step5：
运行Flask

##4.相关文章
####策略算法工程师之路-基于内容的图像检索(CBIR)
https://zhuanlan.zhihu.com/p/158740736
####kmeans图像检索matlab
https://blog.csdn.net/qq_41852441/article/details/106322521

