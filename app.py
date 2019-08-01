#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)

# 不使用 ascii 编码来序列化JSON对象
# 显示中文
app.config['JSON_AS_ASCII'] = False


@app.route("/", methods=["GET"])
def hello():
    return "<h1>Hello World!<h1>"


if __name__ == '__main__':
    app.debug = True
    app.run()
