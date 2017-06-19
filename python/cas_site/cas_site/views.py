""" cas site index page"""
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from user_info import ldap_opt

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

# def page_not_found(request):
#     return render(request,'404.html', {'page_not_found': True})

def page_error(request):
    """IE detect"""
    return render(request, 'ie_detect.html')
