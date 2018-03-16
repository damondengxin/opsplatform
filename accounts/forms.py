#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from django import forms
from django.contrib import auth


from .models import UserInfo, RoleList, PermissionList


class LoginUserForm(forms.Form):
    username = forms.CharField(label='账 号', error_messages={'required': '账号不能为空'},
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='密 码', error_messages={'required': '密码不能为空'},
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None

        super(LoginUserForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('账号密码不匹配')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('此账号已被禁用')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache


class AddUserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('username','password','email','nickname', 'role',"is_superuser", 'is_active',"department","position")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'role': forms.SelectMultiple(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'is_superuser': forms.Select(choices=((True, '是'),(False, '否')),attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'is_active': forms.Select(choices=((True, '启用'),(False, '禁用')),attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),

        }

    def __init__(self,*args,**kwargs):
        super(AddUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].label = '账 号'
        self.fields['username'].error_messages = {'required': '请输入账号'}
        self.fields['password'].label = '密 码'
        self.fields['password'].error_messages={'required': '请输入密码'}
        self.fields['email'].label = '邮 箱'
        self.fields['email'].error_messages = {'required': '请输入邮箱', 'invalid': '请输入有效邮箱'}
        self.fields['nickname'].label = '姓 名'
        self.fields['nickname'].error_messages = {'required': '请输入姓名'}
        self.fields['role'].label = '角 色'
        self.fields["is_superuser"].label ="管理员状态"
        self.fields['is_active'].label = '状 态'
        self.fields["department"].label="部门"
        self.fields["position"].label="职位"

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError('密码必须大于6位')
        return password
    def clean(self):
        cleaned_data = super(AddUserForm, self).clean()
        username = cleaned_data.get('username')
        if UserInfo.objects.filter(username=username):
            self._errors['username'] = self.error_class(["{}已经存在相同的记录".format(username)])
        return cleaned_data

class EditUserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('username', 'email', 'nickname', 'role', "is_superuser",'is_active',"department","position")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'nickname': forms.TextInput(attrs={'class':'form-control', 'style': 'width:50%;'}),
            #'role': forms.Select(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'role': forms.SelectMultiple(attrs={'class': 'form-control', 'size':'20%','style': 'width:50%;'}),
            'is_superuser': forms.Select(choices=((True, '是'), (False, '否')),
                                         attrs={'class': 'form-control', 'style': 'width:50%;'}),

            'is_active': forms.Select(choices=((True, '启用'),(False, '禁用')),attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:50%;'}),
        }

    def __init__(self,*args,**kwargs):
        super(EditUserForm,self).__init__(*args,**kwargs)
        self.fields['username'].label = '账 号'
        self.fields['username'].error_messages = {'required':'请输入账号'}
        self.fields['email'].label = '邮 箱'
        self.fields['email'].error_messages = {'required':'请输入邮箱','invalid':'请输入有效邮箱'}
        self.fields['nickname'].label = '姓 名'
        self.fields['nickname'].error_messages = {'required':'请输入姓名'}
        self.fields["is_superuser"].label = "管理员状态"
        self.fields['role'].label = '角 色'
        self.fields['is_active'].label = '状 态'

    def clean_password(self):
        return self.cleaned_data['password']


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='原密码', error_messages={'required': '请输入原始密码'},
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width:500px;'}))
    new_password1 = forms.CharField(label='新密码', error_messages={'required': '请输入新密码'},
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width:500px;'}))
    new_password2 = forms.CharField(label='新密码', error_messages={'required': '请重复新输入密码'},
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width:500px;'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError('原密码错误')
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if len(password1)<6:
            raise forms.ValidationError('密码必须大于6位')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('两次密码输入不一致')
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class RoleListForm(forms.ModelForm):
    class Meta:
        model = RoleList
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','style':'width:80%'}),
            #'permission': forms.Select(attrs={'class': 'form-control', 'size':'30%','style':'width:80%'}),
        }

    def __init__(self,*args,**kwargs):
        super(RoleListForm,self).__init__(*args, **kwargs)
        self.fields['name'].label = '角色名称'
        self.fields['name'].error_messages = {'required': '请输入名称'}
        # self.fields['permission'].label = 'URL'
        # self.fields['permission'].required = False

    def clean(self):
        cleaned_data = super(RoleListForm, self).clean()
        name= cleaned_data.get('name')
        if RoleList.objects.filter(name=name):
            self._errors['name'] = self.error_class(["{}已经存在相同的记录".format(name)])
        return cleaned_data

class PermissionListForm(forms.ModelForm):
    class Meta:
        model = PermissionList
        exclude = ("id",)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','style': 'width:80%;'}),
            'url': forms.TextInput(attrs={'class': 'form-control','style': 'width:80%;'}),
            'role': forms.Select(attrs={'class': 'form-control', 'style': 'width:80%'})
        }

    def __init__(self, *args, **kwargs):
        super(PermissionListForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = '名 称'
        self.fields['name'].error_messages = {'required':'请输入名称'}
        self.fields['url'].label = 'URL'
        self.fields['url'].error_messages = {'required':'请输入URL'}
        self.fields['role'].label = '角色'


    # def clean(self):
    #     cleaned_data = super(PermissionListForm, self).clean()
    #     name= cleaned_data.get('name')
    #     url= cleaned_data.get('url')
    #     if PermissionList.objects.filter(name=name,url=url):
    #         self._errors['name'] = self.error_class(["{0},{1}已经存在相同的记录".format(name,url)])
    #     return cleaned_data






