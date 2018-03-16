#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import json

from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.mail import  send_mail


from .permission import permission_verify
from .forms import AddUserForm
from .forms import LoginUserForm, EditUserForm, ChangePasswordForm
from .models import UserInfo
from config.api import Config
from opsplatform import settings


def login(request):
    if request.method == 'GET':
        return render(request,'accounts/login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            error = "用户名或密码错误，请重新输入。"
            return render(request,"accounts/login.html",{'error':error})

def register(request):
    if request.method == 'GET':
        return render(request,'accounts/register.html')
    else:
        #print(request.POST)
        username=request.POST.get("username").strip()
        password=request.POST.get("password").strip()
        email=request.POST.get("e-mail").strip()
        nickname=request.POST.get("name").strip()
        department=request.POST.get("department").strip()
        position=request.POST.get("position").strip()
        UserInfo.objects.create_user(email, username, password,nickname=nickname,department=department,position=position)
        return redirect('/accounts/login/')

def usercheck(request):
    if request.method == "POST":
        user_obj = UserInfo.objects.filter(username=request.POST['username']).values('username')
        user = ''
        if user_obj:
            user = user_obj[0]['username']
        return HttpResponse(user)


def forget_password(request):
    if request.method == 'GET':
        return render(request, 'accounts/forget_password.html')
    else:
        username = request.POST['username']
        user = UserInfo.objects.get(username__exact=username)
        pwd = UserInfo.objects.make_random_password(length=12)
        user.set_password(pwd)
        user.save()
        #user.email_user('帐号:{0}', '你的新密码为:{1}'.format(user,pwd))
        msg ='<p>新密码:%s </p>' % pwd
        send_mail('新密码', '', settings.EMAIL_HOST_USER, ["%s" % user.email], html_message=msg)

        return HttpResponse('重置密码完成,请到你的邮箱查看.')


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")


@login_required()
@permission_verify()
def user_list(request):
    all_user = UserInfo.objects.all()
    return render(request, 'accounts/user_list.html',locals())


@login_required
@permission_verify()
def user_add(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            return HttpResponseRedirect("/accounts/user/list/")
        return render(request, "accounts/user_add.html", locals())
    else:
        form = AddUserForm()
        return render(request, 'accounts/user_add.html', locals())

@login_required
@permission_verify()
def user_edit(request, id):
    user = get_user_model().objects.get(id=id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/accounts/user/list/")
        return render(request, "accounts/user_edit.html", locals())
    else:
        form = EditUserForm(instance=user)
        return render(request, 'accounts/user_edit.html', locals())

@login_required
@permission_verify()
def user_del(request):
    ret = {'status': True, 'error': None, 'data': None}
    if request.method == "POST":
        try:
            id=request.POST.get("id")
            for i in json.loads(id):
                get_user_model().objects.get(id=int(i)).delete()
        except Exception as e:
            ret["error"] = str(e)
            ret["status"] = False
        return  HttpResponse(json.dumps(ret))





@login_required
@permission_verify()
def reset_password(request, id):
    user = get_user_model().objects.get(id=id)
    newpassword = get_user_model().objects.make_random_password()
    #print('====>ResetPassword:{}-->{}'.format(user.username, newpassword))
    user.set_password(newpassword)
    user.save()
    msg = '<p>新密码:%s </p> ' %newpassword
    send_mail('新密码', '', Config.email()["email"], ["%s" %user.email ], html_message = msg)

    return HttpResponse('密码已经发送到您的邮箱，注意查收')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('logout'))
    else:
        form = ChangePasswordForm(user=request.user)
        return render(request, 'accounts/change_password.html', locals())
