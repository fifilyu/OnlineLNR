#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
应用程序配置文件
"""

# 用户上传图片保存路径
CFG_UPLOAD_FOLDER = 'public/imgs/uploads'
# 识别结果文件
CFG_RESULT_FOLDER = 'public/imgs/results'
# 默认结果文件
CFG_DEFAULT_RESULT_IMG = '/imgs/online_lnr/default_car.jpg'
# 允许用户上传的图片类型
CFG_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# Flask安全密钥
CFG_SECRET_KEY = b'yYVyoJNNAIighAoRMU7j2MEAEGWUx1nTdVan9n6N'
# 上传最大文件限制2MB
CFG_UPLOAD_LIMIT = 2 * 1024 * 1024
