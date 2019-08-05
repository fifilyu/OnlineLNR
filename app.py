#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import CFG_UPLOAD_FOLDER
from config import CFG_SECRET_KEY
from flask import Flask
from flask import render_template
from flask import jsonify
import views

app = Flask(__name__)

# 不使用 ascii 编码来序列化JSON对象
# 显示中文
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = CFG_SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = CFG_UPLOAD_FOLDER


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/api/recognize", methods=["POST"])
def recognize():
    return jsonify(views.recognize())


if __name__ == '__main__':
    app.debug = True
    app.run()
