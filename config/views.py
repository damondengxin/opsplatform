#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
# import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.contrib.auth import get_user_model


#from api.log import dic
#from accounts.permission import permission_verify
from .api import Config,dic


# @login_required()
# @permission_verify()
def index(request):
    all_level = dic
    result=Config.conf_all()
    return render(request, 'config/config.html', locals())


# @login_required()
# @permission_verify()
def config_save(request):
    ret = {'status': True, 'error': None, 'data': None}
    if request.method == 'POST':
        #print(request.POST)
        if Config.save(request.POST):
            ret["data"]="保存成功"
        else:
            ret["status"] = False
            ret["data"]="保存失败"
        return HttpResponse(json.dumps(ret))
    result = Config.conf_all()
    return render(request, 'config/config.html', locals())


# @login_required()
# @permission_verify()
def get_token(request):
    if request.method == 'POST':
        new_token = get_user_model().objects.make_random_password(length=12, allowed_chars='abcdefghjklmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789')
        return HttpResponse(new_token)
    else:
        return True
