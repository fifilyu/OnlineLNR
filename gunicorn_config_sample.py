#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing

debug = False
loglevel = 'info'
bind = "127.0.0.1:5467"
pidfile = "var/run/gunicorn.pid"
accesslog = "var/log/access.log"
errorlog = "var/log/error.log"
daemon = True

# 启动的进程数
workers = multiprocessing.cpu_count()
