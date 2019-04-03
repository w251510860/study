#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author:wd
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from .celery import app as celery_app
from proj import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')  # 设置django环境
app = Celery('proj')
app.config_from_object('django.conf:settings')  # 使用CELERY_ 作为前缀，在settings中写配置
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  # 发现任务文件每个app下的task.py

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/2'  # Broker配置，使用Redis作为消息中间件
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/3'  # BACKEND配置，这里使用redis
CELERY_RESULT_SERIALIZER = 'json'  # 结果序列化方案
