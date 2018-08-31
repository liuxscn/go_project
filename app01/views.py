
from django.shortcuts import HttpResponse, render, redirect

def login(request):

    # return HttpResponse(request.method + ' hey there')
    # return render(request, 'login.html')
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        if u == 'root' and p == 'root':
            return redirect('/index/')
            # return redirect('https://github.com')
        else:
            return render(request, 'login.html', {'error_msg' : '用户名或密码错误'})

def index(request):

    return render(
        request,
        'index.html',
        {
            'name' : 'alex',
            'users' : ['立志', '理解'],
            'user_dict': {'k1' : 'v1', 'k2' : 'v2'},
            'user_list_dict' : [
                {'id':'1', 'name':'alex', 'email':'alex@qq.com'},
                {'id':'2', 'name':'bran', 'email':'bran@qq.com'},
                {'id':'3', 'name':'chan', 'email':'chan@qq.com'},
            ]
        }
    )
    # return HttpResponse(request.method + ' Index')