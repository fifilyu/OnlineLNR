#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time

import cv2
from pathlib import Path

from PIL import Image
from flask import request
from hyperlpr import HyperLPR_PlateRecogntion
from util import allowed_file
from util import mark_photo
from util import make_api_response
from util import check_uploaded_file1
from util import check_uploaded_file2
from util import save_photo


def recognize():
    """
    处理上传文件并识别车牌号码
    :return: dict
    """
    if not check_uploaded_file1('photo', request.files):
        return make_api_response(1, '未找到匹配的图片')

    photo = request.files.get('photo')

    if not check_uploaded_file2(photo.filename):
        return make_api_response(1, '接收到空图片。请选择上传文件')

    if not (photo and allowed_file(photo.filename)):
        return make_api_response(1, '上传的文件格式无效。')

    relative_path = save_photo(photo)
    path = Path(relative_path)

    if not path.is_file():
        return make_api_response(1, '图片文件上传失败')

    image = Image.open(relative_path)
    img_dpi = "%dx%d" % (image.size[0], image.size[1])
    img_format = image.format
    img_size = "%dKB" % (os.path.getsize(relative_path) / 1024)

    start = time.clock()
    # 识别车牌号码
    image = cv2.imread(relative_path)

    if image is None:
        return make_api_response(status=1,
                                 msg='OpenCV读取图片失败',
                                 result_photo=relative_path,
                                 img_dpi=img_dpi,
                                 img_format=img_format,
                                 img_size=img_size)

    result_list = HyperLPR_PlateRecogntion(image)
    elapsed = "%.2fs" % (time.clock() - start)

    if not (result_list and len(result_list) == 1) or not (result_list[0] and len(result_list[0]) == 3):
        return make_api_response(status=1,
                                 msg='操作成功，但未找到有效车牌号',
                                 result_photo=relative_path,
                                 img_dpi=img_dpi,
                                 img_format=img_format,
                                 img_size=img_size,
                                 used_time=elapsed)

    plate = result_list[0][0]
    confidence = result_list[0][1]
    location = result_list[0][2]

    top_left_x = location[0]
    top_left_y = location[1]

    top_right_x = location[2]
    top_right_y = location[1]

    bottom_right_x = location[2]
    bottom_right_y = location[3]

    bottom_left_x = location[0]
    bottom_left_y = location[3]

    rectangle_point_locations = [
        (top_left_x, top_left_y),
        (top_right_x, top_right_y),
        (bottom_right_x, bottom_right_y),
        (bottom_left_x, bottom_left_y)
    ]

    result_photo = mark_photo(relative_path, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y))

    return make_api_response(status=0,
                             msg='车牌号码识别成功......',
                             plate=plate,
                             confidence=float(confidence),
                             result_photo=result_photo,
                             location=rectangle_point_locations,
                             img_dpi=img_dpi,
                             img_format=img_format,
                             img_size=img_size,
                             used_time=elapsed)
