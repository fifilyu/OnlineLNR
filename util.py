#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import uuid

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from config import CFG_ALLOWED_EXTENSIONS
from config import CFG_RESULT_FOLDER
from config import CFG_UPLOAD_FOLDER
from config import CFG_DEFAULT_RESULT_IMG
from PIL import Image
from PIL import ImageDraw


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


def make_api_response(status: int,
                      msg: str,
                      plate='',
                      confidence=0.0,
                      result_photo=CFG_DEFAULT_RESULT_IMG,
                      location=None,
                      img_dpi=(),
                      img_format='',
                      img_size=0,
                      used_time=0):
    """
    根据参数生成接口数据结构

    :param status: 接口状态。0表示成功
    :param msg: 提示信息
    :param plate: 车牌号码
    :param confidence: 可信度
    :param result_photo: 标记的照片路径
    :param location: 像素位置列表
    :param img_dpi: 图片分辨率
    :param img_format: 图片格式
    :param img_size: 图片大小，单位KB
    :param used_time: 识别车牌消耗时间，单位秒
    :return:
    """
    if location is None:
        location = []

    api_response = {
        'status': status,
        'message': msg,
        'plate': plate,
        'result_photo': result_photo,
        'confidence': ('%.2f%%' % (confidence * 100)),
        'location': location,
        'img_dpi': img_dpi,
        'img_format': img_format,
        'img_size': img_size,
        'used_time': used_time
    }

    return api_response


def save_photo(file_storage: FileStorage):
    """
    保存用户上传的图片
    :param file_storage: 上传文件对象
    :return: 返回文件相对路径
    """
    ext = get_ext(file_storage.filename)
    new_filename = get_new_filename(ext)
    # 转换为安全文件名
    new_filename = secure_filename(new_filename)

    relative_path = os.path.join(CFG_UPLOAD_FOLDER, new_filename)
    file_storage.save(relative_path)

    return relative_path


def draw_rectangle(draw, coordinates, color, width=1):
    """
    画一个矩形，并且可以控制边框线粗细。
    :param draw: ImageDraw 对象
    :param coordinates: 顶部左边和底部右边的坐标值
    :param color: 矩形颜色
    :param width: 矩形边框粗细
    :return: None
    """
    for i in range(width):
        rect_start = (coordinates[0][0] - i, coordinates[0][1] - i)
        rect_end = (coordinates[1][0] + i, coordinates[1][1] + i)
        draw.rectangle((rect_start, rect_end), outline = color)


def mark_photo(old_photo_path: str, top_left: tuple, bottom_right: tuple):
    """
    在识别成功的照片上标记出车牌号坐标。
    :param old_photo_path: 用户上传照片的相对路径
    :param top_left: 矩形顶部左边坐标
    :param bottom_right: 矩形底部右边坐标
    :return: 标记图片相对路径
    """

    ext = get_ext(old_photo_path)
    new_filename = get_new_filename(ext)
    relative_path = os.path.join(CFG_RESULT_FOLDER, new_filename)

    image = Image.open(old_photo_path)
    draw = ImageDraw.Draw(image)
    draw_rectangle(draw, (top_left, bottom_right), color='red', width=10)
    image.save(relative_path)

    return relative_path
