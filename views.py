#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2

from flask import request
from hyperlpr import HyperLPR_PlateRecogntion
from util import allowed_file
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

    if photo and allowed_file(photo.filename):
        file_full_path = save_photo(photo)

        # 识别车牌号码
        image = cv2.imread(file_full_path)
        result_list = HyperLPR_PlateRecogntion(image)

        # 识别成功
        if result_list and len(result_list) == 1:
            if result_list[0] and len(result_list[0]) == 3:
                plate = result_list[0][0]
                confidence = result_list[0][1]
                location = result_list[0][2]

                return make_api_response(status=0,
                                         msg='',
                                         plate=plate,
                                         confidence=float(confidence),
                                         location=location)

    return make_api_response(1, '车牌号码识别失败')
