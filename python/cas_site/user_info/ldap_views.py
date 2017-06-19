from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from . import ldap_opt 
import json

#Query Select 
def ldap_queryselect(request, team, user):
    team_list = []
    allteam_list = []
    group_list = []
    c_ins = ldap_opt.ldap3_connect()    
    dict_user_id = ldap_opt.ldap3_query_user(c_ins)
    dict_groud_id = ldap_opt.ldap3_query_group(c_ins)
    for group, ggid in dict_groud_id.items():
        user_list = []
        if group == team:
            group_list.append({'n': group})
            for usernm, ugid in dict_user_id.items():
              if ggid == ugid[1]:
                  user_list.append({'n': usernm})
            team_list.append({'n': group, 's':user_list})

        alluser_list = []
        for usernm, ugid in dict_user_id.items():
            if ggid == ugid[1]:
                alluser_list.append({'n': usernm})
        allteam_list.append({'n': group, 's':alluser_list})
    allteam_list.append({'n': 'all', 's':[]})
    user_membs = ldap_opt.ldap3_search_membs(c_ins, user)
    if len(user_membs[user]) >0 :
        team_list = [{'n': 'Query', 's': allteam_list},
                     {'n': 'Edit', 's': team_list},
                     {'n': 'Delete', 's': team_list},
                     {'n':'Add', 's': group_list}]
    else:
        team_list = [{'n': 'Query', 's': allteam_list},
                     {'n': 'Edit', 's':[{'n': team, 's':[{'n': user}]}]}]  
    c_ins.unbind()
    return HttpResponse(json.dumps(team_list), content_type='application/json')

#Edit and add information to relative emails 
def send_email(subject, message, recipient_list):
    if subject == "password":
        subject = "User Password Modify--" + message['username']
        message = render_to_string( 'user_info/emailinfo.html' ,{ 'username': message['username'],
                                                                  'password': message['passwd'],
                                                                  'pd_add': True
                                                                  })
        recipient_list = [people + '@cpu.com.cn' for people in recipient_list if people]
        email = EmailMessage(subject, message,'liq@cpu.com.cn', recipient_list)  
    elif subject == "add":
        subject = " Team %s add new member---%s" %(message['team'], message['username'])
        message = render_to_string( 'user_info/emailinfo.html' ,{ 'username': message['username'],
                                                                  'team': message['team'],
                                                                  'manager': message['manager'],
                                                                  'email': message['email'],
                                                                  'telephone': message['tel']
                                                                  }) 
        recipient_list = [people + '@cpu.com.cn' for people in recipient_list if people]
        cc_list = ['liq@cpu.com.cn','liut@cpu.com.cn']
        email = EmailMessage(subject, message,'liq@cpu.com.cn', recipient_list, cc_list)  
    email.content_subtype = "html"
    email.send()        

#person information
def ldap_userinfo(request):
    if request.session.get('usernm', False):
        usernm  = request.session['usernm']
        lpasswd = request.session['passwd']
        c_ins = ldap_opt.ldap3_connect()
        context = ldap_opt.ldap3_search_user(c_ins, usernm)
        context['usernm'] = usernm
        context['lpasswd'] = lpasswd
        context['nav_flag'] = True
        c_ins.unbind()
        return render(request, 'user_info/ldapinfo.html',context)
    else:
        return render(request, 'index.html', {'log_out':True}) 

#team members information
def ldap_allmembers(request):
    if request.session.get('usernm', False):
        usernm = request.session['usernm']
        c_ins = ldap_opt.ldap3_connect()
        userdic = ldap_opt.ldap3_search_user(c_ins, usernm)
        team = userdic['team']
        all_members = ldap_opt.ldap3_search_membs(c_ins, usernm, all_membs = True)
        if len(all_members[usernm]) > 0:
            context ={'content_flag': True, 
                      'usernm':usernm, 
                      'team': team, 
                      'membdata': all_members[usernm]} 
        else:
            context = {'content_flag': True,
                       'usernm':usernm, 
                       'team': team, 
                       'membdata':[{'manager':None,
                                     'email': None,
                                     'tel':None, 
                                     'team':None,
                                      'manager':None }]}
        c_ins.unbind()
        return render(request,'user_info/ldapinfo.html',context)
    else:
        return render(request, 'index.html', {'log_out':True})

#members operations based on ajax
@csrf_exempt
def ldap_ajaxmembers(request):
    if request.session.get('usernm', False):
        usernm = request.session['usernm']
        ajax_op = request.GET.get('operation')
        ajax_tm = request.GET.get('team')
        ajax_user = request.GET.get('user')
        c_ins = ldap_opt.ldap3_connect()        
        if ajax_op == "Query":
            if ajax_user == None:
                if ajax_tm == 'all':
                    query_membs = ldap_opt.ldap3_search_membs(c_ins, ajax_tm, all_membs = True)
                else:      
                    query_membs = ldap_opt.ldap3_search_membs(c_ins, ajax_tm, sg_memb = False) 
                if len(query_membs[ajax_tm]) > 0:
                    query_membs = query_membs[ajax_tm] 
                else:
                    query_membs = [{'username':'None', 
                                   'email': 'None',
                                   'tel':'None',
                                   'team':'None', 
                                   'manager':'None'}]
            else:
                query_membs = ldap_opt.ldap3_search_user(c_ins, ajax_user)
            c_ins.unbind()
            return HttpResponse(json.dumps(query_membs), content_type='application/json')
        elif ajax_op == "Add":
            if request.method == "GET":
                add_membs = ldap_opt.ldap3_search_user(c_ins, usernm)
                add_membs['usernm'] = usernm
                add_membs['username'] = 'name'
                add_membs['tel'] = '123456'
                add_membs['manager'] = usernm
                add_membs['passwd'] = 'nfs123'
                c_ins.unbind()
                return HttpResponse(json.dumps(add_membs), content_type = 'application/json')
        elif ajax_op == "Edit":
            if request.method == "GET":
                edit_membs = ldap_opt.ldap3_search_user(c_ins, ajax_user)
                c_ins.unbind()
                return HttpResponse(json.dumps(edit_membs), content_type = 'application/json')
        elif ajax_op == "Delete":
            if request.method == "GET":
                delete_mems = ldap_opt.ldap3_search_user(c_ins, ajax_user)
                c_ins.unbind()
                return HttpResponse(json.dumps(delete_mems), content_type = 'application/json')
    else:
        return render(request, 'index.html', {'log_out':True})

#user password modify
def ldap_pdmodify(request):
    if request.session.get('usernm', False):
        c_ins = ldap_opt.ldap3_connect()
        if request.method == "GET":
            usernm = request.session['usernm']
            userdic = ldap_opt.ldap3_search_user(c_ins, usernm)
            context = {'usernm': usernm, 
                       'team': userdic['team'],
                       'nav_flag': True,
                       'pw_modify':True}
            c_ins.unbind()
            return render(request, 'user_info/ldapinfo.html',context)
        elif request.method == "POST":
            usernm = request.POST.get('ldapnm')
            password = request.POST.get('passwd')
            userinfo_dic = {'username': usernm, 'passwd': password}
            context = ldap_opt.ldap3_modify(c_ins, userinfo_dic, 'Passwd')
            context['usernm'] = usernm
            context['passwd'] = password
            context['nav_flag'] = True
            context['pw_modify'] = True
            context['pd_success'] = True
            send_email('password', userinfo_dic, [usernm])
            c_ins.unbind()
            return render(request, 'user_info/ldapinfo.html',context)            
    else:
      return render(request, 'index.html', {'log_out':True})

#members update personal informations 
@csrf_exempt
def ldap_membupdate(request):
    if request.session.get('usernm', False):    
        usernm = request.session['usernm']    
        c_ins = ldap_opt.ldap3_connect()        
        if request.method == 'POST':
            member = request.POST.get('ldapnm')
            userinfo_dic = {'username': member, 'tel':request.POST.get('ldaptel')}
            context = ldap_opt.ldap3_modify(c_ins, userinfo_dic, 'Edit')
            context['usernm'] = usernm
            context['update_success'] = True
            c_ins.unbind()
            return render(request, 'user_info/ldapinfo.html',context)
    else:
        return render(request, 'index.html', {'log_out':True})

#delete resignation people
@csrf_exempt
def ldap_userdelete(request):
    if request.session.get('usernm', False):    
        usernm = request.session['usernm']    
        c_ins = ldap_opt.ldap3_connect()        
        if request.method == 'POST':
            member = request.POST.get('ldapnm')
            userinfo_dic = {'username': member}
            if  member == 'on-job':
                userinfo_dic['state'] = '0'.encode()
            else:
                userinfo_dic['state'] = '1'.encode()
            context = ldap_opt.ldap3_modify(c_ins, userinfo_dic, 'Delete')
            context['usernm'] = usernm
            context['delete_success'] = True
            c_ins.unbind()
            return render(request, 'user_info/ldapinfo.html',context)
    else:
        return render(request, 'index.html', {'log_out':True})

#add new members into relative team
@csrf_exempt
def ldap_useradd(request):
    if request.session.get('usernm', False):    
        usernm = request.session['usernm']    
        c_ins = ldap_opt.ldap3_connect()                        
        if request.method == 'GET':
            context = ldap_opt.ldap3_search_user(c_ins, usernm)
            context['usernm'] = usernm
            context['username'] = 'name'
            context['tel'] = '123456'
            context['passwd'] = 'nfs123'
            context['adduser'] = True
            c_ins.unbind()
            return render(request, 'user_info/ldapinfo.html',context)
        elif request.method == 'POST':
            member = request.POST.get('ldapnm') 
            if member in ldap_opt.ldap3_query_user(c_ins, allusers = True):
                context = ldap_opt.ldap3_search_user(c_ins, usernm)
                context['usernm'] = usernm
                context['username'] = member
                context['tel'] = '123456'
                context['passwd'] = 'nfs123'
                context['adduser'] = True
                context['add_fail'] = True
                c_ins.unbind() 
                return render(request, 'user_info/ldapinfo.html', context)
            else:
                newuser = {'username': member, 
                           'tel': request.POST.get('ldaptel'),
                           'state':request.POST.get('ldapst'),
                           'manager': request.POST.get('ldapmg'), 
                           'team':request.POST.get('ldaptm'),
                           'password':'nfs123'}
                ldap_opt.ldaps_add_users(c_ins, newuser)
                context = newuser
                context['usernm'] = usernm 
                context['manager'] = context['manager'].split(',')[0].split('=')[1] 
                context['add_success'] = True
                send_email('add', context, [usernm, member])
                c_ins.unbind()
                return render(request, 'user_info/ldapinfo.html', context)
    else:
        return render(request, 'index.html', {'log_out':True})



