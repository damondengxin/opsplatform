#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import RoleListForm
from .models import RoleList
from accounts.permission import permission_verify



@login_required
@permission_verify()
def role_list(request):
    all_role = RoleList.objects.all()
    return render(request, 'accounts/role_list.html', locals())

@login_required
@permission_verify()
def role_add(request):
    if request.method == "POST":
        form = RoleListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('role_list'))
        return render(request, 'accounts/role_add.html', locals())
    else:
        form = RoleListForm()
        return render(request, 'accounts/role_add.html', locals())



@login_required
@permission_verify()
def role_edit(request, id):
    print(id)
    iRole = RoleList.objects.get(id=id)
    if request.method == "POST":
        form = RoleListForm(request.POST, instance=iRole)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('role_list'))
        return render(request, 'accounts/role_edit.html', locals())
    else:
        form = RoleListForm(instance=iRole)
        return render(request, 'accounts/role_edit.html', locals())




@login_required
@permission_verify()
def role_del(request):
    ret = {'status': True, 'error': None, 'data': None}
    if request.method == "POST":
        try:
            id=request.POST.get("id")
            for i in json.loads(id):
                RoleList.objects.get(id=int(i)).delete()
        except Exception as e:
            ret["error"] = str(e)
            ret["status"] = False
        return  HttpResponse(json.dumps(ret))