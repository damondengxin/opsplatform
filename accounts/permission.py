#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import PermissionListForm
from .models import UserInfo, RoleList, PermissionList


def permission_verify():
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            userobj = UserInfo.objects.get(username=request.user)
            if not userobj.is_superuser:
                if not userobj.role.all():
                    return HttpResponseRedirect(reverse('noperm'))
                rolelist =userobj.role.all()
                #role_permission_list = role_permission.permission.all()
                matchUrl = []
                #requesturl = request.build_absolute_uri()
                requesturl=request.get_full_path()
                #print(requesturl)
                for x in rolelist:
                    for u in PermissionList.objects.filter(role=x):
                        if requesturl == u.url or requesturl.rstrip('/') == u.url:
                            matchUrl.append(u.url)
                        elif requesturl.startswith(u.url):
                            matchUrl.append(u.url)
                        else:
                            pass
                #print('{}---->matchUrl:{}'.format(request.user, str(matchUrl)))
                if not matchUrl:
                    return HttpResponseRedirect(reverse('noperm'))
            else:
                pass
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



@login_required
@permission_verify()
def permission_list(request):
    all_permission = PermissionList.objects.all()
    return render(request, 'accounts/permission_list.html', locals())

@login_required
@permission_verify()
def permission_add(request):
    if request.method == "POST":
        form = PermissionListForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('permission_list'))
        return render(request,'accounts/permission_add.html', locals())
    else:
        form = PermissionListForm()
        return render(request, 'accounts/permission_add.html', locals())


@login_required
@permission_verify()
def permission_edit(request, id):
    iPermission = PermissionList.objects.get(id=id)
    if request.method == "POST":
        form = PermissionListForm(request.POST, instance=iPermission)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('permission_list'))
        return render(request, 'accounts/permission_edit.html', locals())
    else:
        form = PermissionListForm(instance=iPermission)
        return render(request, 'accounts/permission_edit.html', locals())


@login_required
@permission_verify()
def permission_del(request):
    ret = {'status': True, 'error': None, 'data': None}
    if request.method == "POST":
        try:
            id=request.POST.get("id")
            for i in json.loads(id):
                PermissionList.objects.get(id=int(i)).delete()
        except Exception as e:
            ret["error"] = str(e)
            ret["status"] = False
        return  HttpResponse(json.dumps(ret))