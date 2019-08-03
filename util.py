#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import uuid

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from config import CFG_ALLOWED_EXTENSIONS
from config import CFG_UPLOAD_FOLDER


def get_ext(filename):
    """
    获取用户上传文件的名称
    :param filename: 文件名称
    :return: str
    """
    return filename.rsplit('.', 1)[1].lower()


def allowed_file(filename):
    """
    用户只能上传允许的文件类型
    :param filename: 文件名称
    :return: bool
    """
    ext = get_ext(filename)
    return '.' in filename and ext in CFG_ALLOWED_EXTENSIONS


def gen_random_str():
    """
    生成随机字符串
    :return: str
    """
    unique_filename = str(uuid.uuid4())
    filename = unique_filename.replace('-', '')

    return filename


def get_new_filename(ext: str):
    """
    生成随机文件名
    :param ext: 文件扩展名，如jpg、png等
    :return: str
    """
    return gen_random_str() + '.' + ext


def check_uploaded_file1(name: str, file_list: list):
    """
    检查上传的文件列表中是否存在指定的文件。
    :param  name: 文件名称
    :param  file_list: 文件列表
    :return:
    """
    return name in file_list


def check_uploaded_file2(filename: str):
    """
    检查用户上传的文件名称是否为空。
    :param  filename: 用户上传的文件名称
    :return:
    """
    return filename != ''


def make_api_response(status: int, msg: str, plate='', confidence=0.0, location=None):
    """
    根据参数生成接口数据结构

    :param status: 接口状态。0表示成功，1表示失败
    :param msg: 提示信息
    :param plate: 车牌号码
    :param confidence: 可信度
    :param location: 像素位置列表
    :return:
    """

    if location is None:
        location = []
    api_response = {
        'status': status if status in [0, 1] else 1,
        'message': msg,
        'plate': plate,
        'confidence': confidence,
        'location': location
    }

    return api_response


def save_photo(file_storage: FileStorage):
    """
    保存用户上传的图片
    :param file_storage: 上传文件对象
    :return: 返回文件保存绝对路径
    """
    ext = get_ext(file_storage.filename)
    new_filename = get_new_filename(ext)
    # 转换为安全文件名
    new_filename = secure_filename(new_filename)

    # 绝对路径文件名
    file_full_path = os.path.abspath(os.path.join(CFG_UPLOAD_FOLDER, new_filename))
    file_storage.save(file_full_path)

    return file_full_path
