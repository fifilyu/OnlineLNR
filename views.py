#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
from pathlib import Path

import cv2
import hyperlpr3 as lpr3
from PIL import Image
from flask import request

from util import allowed_file
from util import check_uploaded_file1
from util import check_uploaded_file2
from util import check_uploaded_file3
from util import make_api_response
from util import mark_photo
from util import save_photo


def recognize():
    """
    处理上传文件并识别车牌号码
    :return: dict
    """
    if not check_uploaded_file1('photo', request.files):
        return make_api_response(2, '未找到匹配的图片')

    photo = request.files.get('photo')

    if not check_uploaded_file2(photo.filename):
        return make_api_response(2, '未接收到任何图片，请重新上传图片')

    if not (photo and allowed_file(photo.filename)):
        return make_api_response(2, '上传的文件格式无效。')

    relative_path = save_photo(photo)
    photo_path = Path(relative_path)

    if not photo_path.is_file():
        return make_api_response(2, '图片文件上传失败')

    if not check_uploaded_file3(relative_path):
        return make_api_response(2, '图片大小为0，请重新上传图片')

    image = Image.open(relative_path)
    img_dpi = "%dx%d" % (image.size[0], image.size[1])
    img_format = image.format
    img_size = "%dKB" % (os.path.getsize(relative_path) / 1024)

    start = time.process_time()
    # 识别车牌号码
    image = cv2.imread(relative_path)

    if image is None:
        return make_api_response(status=1,
                                 msg='OpenCV读取图片失败',
                                 result_photo=photo_path.name,
                                 img_dpi=img_dpi,
                                 img_format=img_format,
                                 img_size=img_size)

    catcher = lpr3.LicensePlateCatcher()
    result_list = catcher(image)
    elapsed = "%.2fs" % (time.process_time() - start)

    if not (result_list and len(result_list) == 1) or not (result_list[0] and len(result_list[0]) == 4):
        return make_api_response(status=1,
                                 msg='操作成功，但未找到有效车牌号',
                                 result_photo=photo_path.name,
                                 img_dpi=img_dpi,
                                 img_format=img_format,
                                 img_size=img_size,
                                 used_time=elapsed)

    plate = result_list[0][0]
    confidence = result_list[0][1]
    location = result_list[0][3]

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
                             result_photo=Path(result_photo).name,
                             location=rectangle_point_locations,
                             img_dpi=img_dpi,
                             img_format=img_format,
                             img_size=img_size,
                             used_time=elapsed)
