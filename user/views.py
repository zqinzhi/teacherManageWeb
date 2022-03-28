from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def loginView(request):
    # 设置标题和另外两个URL链接
    unit_l = '/user/setpassword.html'
    unit_1_name = '修改密码'
    unit_2_name = ''
    unit_2_psw = ''
    if request.method == "POST":
        print('我是post')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if User.objects.filter(username=username):
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                return redirect("/teachersManage/1/")
            else:
                tips = '账号密码错误，请重新输入'
        else:
            tips = '用户不存在，请联系管理员'
    return render(request, 'user.html ', locals())

def registerView(request):
    return render(request, 'teachersShowHtml.html', locals())

def setpasswordView(request):
    return render(request, 'teachersShowHtml.html', locals())

def logoutView(request):
    return render(request, 'teachersShowHtml.html', locals())
