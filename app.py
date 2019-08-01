#!/usr/bin/env python3

# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template

app = Flask(__name__)

# 不使用 ascii 编码来序列化JSON对象
# 显示中文
app.config['JSON_AS_ASCII'] = False


@app.route("/", methods=["GET"])
def hello():
    return render_template("index.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
