#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms
from .models import website


class website_form(forms.ModelForm):

    def clean(self):
        cleaned_data = super(website_form, self).clean()
        name = cleaned_data.get('name')
        url = cleaned_data.get('url')
        if website.objects.filter(name=name, url=url):
            self._errors['name'] = self.error_class(["%s的信息已经存在" % name])
        return cleaned_data

    class Meta:
        model = website
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'url': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
        }

