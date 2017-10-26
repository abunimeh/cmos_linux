""" cas site index page"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from user_info import ldap_opt
from pj_app.models import Comment, User

def login_auth(request):
    """user auth and login """
    if request.method == 'GET':
        usernm = request.GET.get('username')
        password = request.GET.get('password')
        c_ins = ldap_opt.ldap3_connect()
        user = authenticate(username=usernm, password=password)
        if user is not None:
            login(request, user)
            request.session['usernm'] = usernm
            request.session['passwd'] = password
            context = ldap_opt.ldap3_search_user(c_ins, usernm)
            context['usernm'] = usernm
            context['lpasswd'] = password
            context['nav_flag'] = True
            c_ins.unbind()
            return render(request, 'user_info/ldapinfo.html', context)
        c_ins.unbind()
        return render(request, 'index.html', {'log_error':True})

def logout_auth(request):
    """user logout"""
    logout(request)
    return render(request, 'index.html')

def contact(request):
    """ vp contact page """
    return render(request, 'contact.html')


def page_error(request):
    """IE detect"""
    return render(request, 'ie_detect.html')

@csrf_exempt
def comments(request):
    """user commments"""
    com_lst = []
    if request.method == "GET":
        number = int(request.GET.get("number"))
        for com_obj in Comment.objects.order_by("-id")[number-5:number]:
            com_lst.append({"name": com_obj.user.name,
                            "comment": com_obj.comment,
                            "time": com_obj.pub_time
                           })
    elif request.method == "POST":
        user = request.POST.get("name")
        comment = request.POST.get("comment")
        pub_time = request.POST.get("time")
        user_obj, _ = User.objects.update_or_create(name=user)
        Comment.objects.create(user=user_obj,
                               comment=comment,
                               pub_time=pub_time)
    return JsonResponse(com_lst, safe=False)
