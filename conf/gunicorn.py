#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing
import os



bind = "127.0.0.1:8001"
workers = multiprocessing.cpu_count() * 2 + 1
backlog = 2048
worker_class = "gthread"
worker_connections = 1000
threads = multiprocessing.cpu_count() * 3
timeout = 300
log_dir = "/var/log/opsmgtv2/gunicorn"

timeout = 120
log_dir = "/var/log/opsmgtv2/gunicorn"
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

accesslog = os.path.join(log_dir, "access.log")
errorlog = os.path.join(log_dir, "error.log")
