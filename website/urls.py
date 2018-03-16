#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from django.urls import path
from . import views

urlpatterns = [
    path('', views.site, name='website'),
    path('add/', views.add, name='website_add'),
    path('delete/', views.delete, name='website_delete'),
    path('edit/<int:id>/', views.edit, name='website_edit'),
    path('save/', views.save, name='website_save'),
]
