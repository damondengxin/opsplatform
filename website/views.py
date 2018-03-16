#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect,reverse
from .models import website
from .forms import website_form
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify


@login_required()
def site(request):
    allwebsite = website.objects.all()
    return render(request, "website/site.html", locals())


@login_required()
@permission_verify()
def add(request):
    if request.method == "POST":
        form = website_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/website/")
        return render(request, "website/add.html", locals())
    else:
        form = website_form()
        return render(request, "website/add.html", locals())


@login_required
@permission_verify()
def edit(request, id):
    obj = website.objects.get(id=id)
    if request.method == "POST":
        form = website_form(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('website'))
        return render(request, 'website/edit.html', locals())
    else:
        form = website_form(instance=obj)
        return render(request, 'website/edit.html', locals())


@login_required()
@permission_verify()
def delete(request):
    ret = {'status': True, 'error': None, 'data': None}
    if request.method == 'POST':
        #print(request.POST)
        try:
            website_items = json.loads(request.POST.get('id'))
            for id in website_items:
                website.objects.filter(id=id).delete()
        except Exception as e:
            ret["status"] = False
            ret["data"] ="删除出错:"+str(e)
        return HttpResponse(json.dumps(ret))


@login_required()
@permission_verify()
def save(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        url = request.POST.get('url')
        item = website.objects.get(id=id)
        item.name = name
        item.url = url
        item.save()
        return redirect("/website/")

