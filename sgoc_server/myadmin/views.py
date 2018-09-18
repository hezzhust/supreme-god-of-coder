# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from .froms import UserForm,LoginForm

home_url = "home/"
login_url = 'login/'
register_path = "myadmin/register.html"
login_path = "myadmin/login.html"

# 注册
def register_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            # 获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password_check = form.cleaned_data['password_check']
            email = form.cleaned_data['email']
            context['username'] = username
            #判断密码是否一致
            if password != password_check:
                context['passwordDifference'] = True
                return render(req, register_path, context)

            # 判断用户是否已注册
            count = User.objects.filter(username=username).count();
            if count:
                context['userExit'] = True
                return render(req, register_path, context)

            # user = auth.authenticate(username=username, password=password)
            # if user:
            #     context['userExit'] = True
            #     return render(req, register_path, context)
            # 添加到数据库（还可以加一些字段的处理）
            user = User.objects.create_user(username=username, password=make_password(password), email = email)
            user.save()

            # 添加到session
            req.session['username'] = username  # 调用auth登录
            auth.login(req, user)
            # 重定向到首页
            return redirect(home_url)

    else:
        context = {'isLogin': False}
        context['passwordDifference'] = False
    # 将req 、页面 、以及context{}（要传入html文件中的内容包含在字典里）返回
    return render(req, register_path, context)
# 登入
def login_view(req):
    context = {}
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            # 获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = authenticate(username=username, password=password)
            if user:
                # 比较成功，跳转index
                auth.login(req, user)
                req.session['username'] = username
                return redirect(home_url)
            else:
                # 比较失败，还在login
                context = {'isLogin': False, 'pawd': False}
                return render(req, login_path, context)
    else:
        context = {'isLogin': False, 'pswd': True}
    return render(req, login_path, context)


# 登出
@login_required
def logout_view(req):
    # 清理cookie里保存username
    auth.logout(req)
    return redirect(login_url)



# 权限校验
# def permission_validate(func):
#     # user = request.POST.user
#     def warpper(request, *args, **kwargs):
#         # FBV 不太清楚为什么要写两次u，可能是内部吧？如果是正常的装饰器应该一次就够了
#         user = request.user
#         username = request.session.get('username') #session中取数据
#         u = request.get_signed_cookie('username', salt='user', default=None) # cookie中取数据
#
#         if not u:
#             return render(request, 'login.html')
#         return func(request, *args, **kwargs)
#     return warpper
