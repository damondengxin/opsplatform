#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='config'),
    path('config_save/', views.config_save, name='config_save'),
    path('token/', views.get_token, name='token'),
]