import itertools
import json
from collections import defaultdict
from ldap3 import ALL, Server, Connection
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Dir, User, Group, Auth, Proj, Level, Repos
from .forms import UserForm, GroupForm, ProjForm, LevelForm, ReposForm

def gen_manager_user_info():
    server = Server(settings.AUTH_LDAP_SERVER_URI, get_info=ALL)
    userdn = settings.AUTH_LDAP_BIND_DN
    passwd = settings.AUTH_LDAP_BIND_PASSWORD
    c_ins = Connection(server, user=userdn, password=passwd, auto_bind=True)
    c_ins.search(search_base=settings.OU,
                 search_filter='(objectclass=person)', attributes=['uid', 'userPKCS12', 'manager'])
    p_entries = c_ins.entries
    p_entries.sort()
    manager_user_dict = defaultdict(list)
    for pp_entry in p_entries:
        ### flag, 0 is normal valid
        if pp_entry.entry_attributes_as_dict.get('userPKCS12')[0] == b'0':
            manager = pp_entry.manager.value.split(',')[0].split('=')[1]
            manager_user_dict[manager].append(pp_entry.uid.value)
    return manager_user_dict

@csrf_exempt
def query_insert_dir(request):
    if request.method == 'POST':
        dir_dict = json.loads(request.body.decode())
        proj_obj, _ = Proj.objects.get_or_create(name=dir_dict['Proj'])
        repos_obj, _ = Repos.objects.get_or_create(name=dir_dict['Repos'])
        lv_obj, _ = Level.objects.get_or_create(name=dir_dict['Level'])
        gp_obj, _ = Group.objects.get_or_create(name=dir_dict['Group'])
        auth_obj, _ = Auth.objects.get_or_create(name=dir_dict['Auth'])
        Dir.objects.create(
            name=dir_dict['Dir'],
            repos=repos_obj,
            proj=proj_obj,
            level=lv_obj,
            group=gp_obj,
            auth=auth_obj)
    return HttpResponse(json.dumps({}), content_type='application/json')

@csrf_exempt
def query_insert_user(request):
    if request.method == 'POST':
        user_dict = json.loads(request.body.decode())
        lv_obj, _ = Level.objects.get_or_create(name=user_dict['Level'])
        gp_obj, _ = Group.objects.get_or_create(name=user_dict['Group'])
        proj_obj, _ = Proj.objects.get_or_create(name=user_dict['Proj'])
        repos_obj, _ = Repos.objects.get_or_create(name=user_dict['Repos'])
        User.objects.create(
            name=user_dict['User'],
            repos=repos_obj,
            proj=proj_obj,
            level=lv_obj,
            group=gp_obj)
    return HttpResponse(json.dumps({}), content_type='application/json')

#####select plugin#####
def svn_query_select(request):
    proj_lst, repos_lst = [], []
    for proj_obj in Proj.objects.all():
        proj_lst.append({"n": proj_obj.name})
    for repos_obj in Repos.objects.all():
        repos_lst.append({"n": repos_obj.name, "s":proj_lst})
    query_lst = [{"n": "Users", "s": repos_lst}, {"n": "Groups", "s": repos_lst}]
    return HttpResponse(json.dumps(query_lst), content_type='application/json')

#####query table info#####
def svn_query_table(type, repos, proj, ugflag=False):
    dir_lst = []
    if type == "Groups":
        if proj == 'all' and repos == 'all':
            dir_qs = Dir.objects.all()
        elif proj == 'all':
            dir_qs = Dir.objects.filter(repos__name=repos)
        elif repos == 'all':
            dir_qs = Dir.objects.filter(proj__name=proj)
        else:
            dir_qs = Dir.objects.filter(repos__name=repos).filter(proj__name=proj)
        for dir_obj in dir_qs:
            dir_lst.append({'directory': dir_obj.name,
                            'project': dir_obj.proj.name,
                            'repository': dir_obj.repos.name,
                            'userpg': dir_obj.group.name,
                            'auth': dir_obj.auth.name,
                            'level': dir_obj.level.name})
    elif type == 'Users':
        proj_lst, repos_lst, level_lst, group_lst = [], [], [], []
        for level_obj in Level.objects.all():
            level_lst.append(level_obj)
        for group_obj in Group.objects.all():
            group_lst.append(group_obj)
        if repos == 'all':
            for repos_obj in Repos.objects.all():
                repos_lst.append(repos_obj)
        else:
            repos_lst.append(repos)
        if proj == 'all':
            for proj_obj in Proj.objects.all():
                proj_lst.append(proj_obj)
        else:
            proj_lst.append(proj)
        plg_lst = itertools.product(proj_lst, repos_lst, level_lst, group_lst)
        for plg_tup in plg_lst:
            user_qs = User.objects.filter(proj__name=plg_tup[0],
                                          repos__name=plg_tup[1],
                                          level__name=plg_tup[2],
                                          group__name=plg_tup[3])
            dir_qs = Dir.objects.filter(proj__name=plg_tup[0],
                                        repos__name=plg_tup[1],
                                        level__name=plg_tup[2],
                                        group__name=plg_tup[3])
            if user_qs.exists() and dir_qs.exists():
                ud_lst = itertools.product(user_qs, dir_qs)
                for ud_tup in ud_lst:
                    dir_lst.append({'directory': ud_tup[1].name,
                                    'project': ud_tup[1].proj.name,
                                    'repository': ud_tup[1].repos.name,
                                    'userpg': ud_tup[0].name,
                                    'group': ud_tup[1].group.name,
                                    'auth': ud_tup[1].auth.name,
                                    'level': ud_tup[1].level.name})
    return dir_lst

#####query one team user info #####
def svn_query_uteam_table(lst):
    auth_lst, noauth_lst = [], []
    for user in lst:
        user_qs = User.objects.filter(name=user)
        if user_qs.exists():
            for user_obj in user_qs:
                auth_lst.append({'userpg': user_obj.name,
                                 'project': user_obj.proj.name,
                                 'repository': user_obj.repos.name,
                                 'group': user_obj.group.name,
                                 'level': user_obj.level.name,
                                 'pk': user_obj.pk})
        else:
            noauth_lst.append(user)
    auth_dict = {'auth': auth_lst, 'noauth': noauth_lst}
    return auth_dict

#####ajax to query info#####
def svn_ajax_userinfo(request):
    if request.session.get('usernm', False):
        types = request.GET.get('type')
        project = request.GET.get('project')
        repository = request.GET.get('repository')
        if types == "Groups":
            svn_querydata = svn_query_table(types, repository, project)
            return HttpResponse(json.dumps(svn_querydata), content_type='application/json')
        elif types == "Users":
            svn_querydata = svn_query_table(types, repository, project, ugflag=True)
            return HttpResponse(json.dumps(svn_querydata), content_type='application/json')
    else:
        return render(request, 'index.html', {'log_out':True})

#####query all teams users info#####
def svn_user_info(request):
    if request.session.get('usernm', False):
        username = request.session['usernm']
        svn_querydata = svn_query_table('Users', 'all', 'all', ugflag=True)
        ### user only can query self info excpet manager
        team_users = gen_manager_user_info()
        if username in team_users:
            return render(request, "user_info/svninfo.html", {'usernm': username,
                                                              'dirinfo': svn_querydata})
        else:
            user_svn_data = [i for i in svn_querydata if i['userpg'] == username]
            return render(request, "user_info/svninfo.html", {'usernm': username,
                                                              'dirinfo': user_svn_data})
    else:
        return render(request, 'index.html', {'log_out':True})

#####personal info#####
def svn_user_query(request):
    if request.session.get('usernm', False):
        username = request.session['usernm']
        team_users = gen_manager_user_info()
        if username in team_users:
            svn_query_data = svn_query_uteam_table(team_users[username])
            lead_flg = True
        else:
            svn_query_data = svn_query_uteam_table([username])
            lead_flg = False
        auth_flg = True if len(svn_query_data['noauth']) else False
        return render(request, "user_info/svn_user_info.html", {'usernm': username,
                                                                'dirinfo': svn_query_data,
                                                                'auth_flg':auth_flg,
                                                                'lead_flg':lead_flg})
    else:
        return render(request, 'index.html', {'log_out':True})

#####user edit#####
def svn_user_update(request, pk):
    if request.session.get('usernm', False):
        username = request.session['usernm']
        if request.method == 'POST':
            post_dic = request.POST
            db_obj = User.objects.get(id=pk)
            db_dic = {'name': db_obj.name,
                      'proj':db_obj.proj.pk,
                      'repos':db_obj.repos.pk,
                      'level':db_obj.level.pk,
                      'group':db_obj.group.pk}
            user_form = UserForm(post_dic, initial=db_dic)
            if not user_form.has_changed() or user_form.is_valid():
                user_form = UserForm(post_dic, instance=User.objects.get(id=pk))
                user_form.save()
                if 'add_another' in post_dic:
                    return HttpResponseRedirect(reverse('user_info:svn_user_add'))
                elif 'editing' in post_dic:
                    return render(request, "user_info/svn_user_edit.html", {'usernm': username,
                                                                            'user_pk':pk,
                                                                            'chg_sucs':True,
                                                                            'form': user_form})
                elif 'edit_save' in post_dic:
                    return HttpResponseRedirect(reverse('user_info:svn_user_query'))
            else:
                return render(request, "user_info/svn_user_edit.html", {'usernm': username,
                                                                        'user_pk':pk,
                                                                        'form': user_form})
        elif request.method == 'GET':
            user_form = UserForm(instance=User.objects.get(id=pk))
            return render(request, "user_info/svn_user_edit.html", {'usernm': username,
                                                                    'user_pk':pk,
                                                                    'form': user_form})
    else:
        return render(request, 'index.html', {'log_out':True})        

#####user add#####
def svn_user_add(request):
    if request.session.get('usernm', False):
        username = request.session['usernm']
        if request.method == 'POST':
            post_dic = request.POST
            user_form = UserForm(post_dic)
            if user_form.is_valid():
                user_form = user_form.save(commit=True)
                #add_more_level(post_dic)
                if 'add_another' in post_dic:
                    return HttpResponseRedirect(reverse('user_info:svn_user_add'))
                elif 'editing' in post_dic:
                    return HttpResponseRedirect(reverse('user_info:svn_user_update',
                                                        kwargs={'pk':user_form.pk}))
                elif 'edit_save' in post_dic:
                    return HttpResponseRedirect(reverse('user_info:svn_user_query'))
            else:
                return render(request, "user_info/svn_user_add.html", {'usernm': username,
                                                                       'form': user_form})
        elif request.method == 'GET':
            user_form = UserForm()
            return render(request, "user_info/svn_user_add.html", {'usernm': username,
                                                                   'form': user_form})
    else:
        return render(request, 'index.html', {'log_out':True})        

#####user delete#####
def svn_user_delete(request, pk):
    if request.session.get('usernm', False):
        username = request.session['usernm']
        user_obj = User.objects.get(id=pk)
        if request.method == 'POST':
            post_dic = request.POST
            if 'delete' in post_dic:
                user_obj.delete()
                return HttpResponseRedirect(reverse('user_info:svn_user_query'))
            elif 'no_delete' in post_dic:
                return HttpResponseRedirect(reverse('user_info:svn_user_update', kwargs={'pk':pk}))
        elif request.method == 'GET':
            return render(request, 'user_info/svn_user_delete.html', {'usernm': username,
                                                                      'del_user': user_obj.name})
    else:
        return render(request, 'index.html', {'log_out':True})        

#####project ,level, group add and change#####
def svn_items_add_update(request, items, pk="pk"):
    if request.session.get('usernm', False):
        username = request.session['usernm']
        def form_items(form_obj, model_obj):
            add_flg = False
            if request.method == 'POST':
                if pk == "pk":
                    add_flg = True
                    item_form = form_obj(request.POST)
                else:
                    db_nm = model_obj.objects.get(id=pk).name
                    item_form = form_obj(request.POST, initial={'name': db_nm})
                if pk == "pk" and item_form.is_valid():
                    new_form = item_form.save(commit=True)
                    return render(request, "user_info/svn_add_or_change_items.html",
                                  {'usernm': username, 'pk':new_form.pk, 'item_temp': items,
                                   'form': item_form, 'add_flg':add_flg})
                elif not item_form.has_changed() or item_form.is_valid():
                    item_form = form_obj(request.POST, instance=model_obj.objects.get(id=pk))
                    item_form.save()
                    return render(request, "user_info/svn_add_or_change_items.html",
                                  {'usernm': username, 'pk':pk, 'item_temp': items,
                                   'form': item_form, 'add_flg':add_flg})
                else:
                    return render(request, "user_info/svn_add_or_change_items.html",
                                  {'usernm': username, 'item_temp': items,
                                   'form': item_form, 'add_flg':add_flg})
            elif request.method == 'GET':
                if pk == "pk":
                    add_flg = True
                    item_form = form_obj()
                else:
                    item_form = form_obj(instance=model_obj.objects.get(id=pk))
                return render(request, "user_info/svn_add_or_change_items.html",
                              {'usernm': username, 'item_temp': items,
                               'form': item_form, 'add_flg':add_flg})
        if items == "Project":
            return form_items(ProjForm, Proj)
        elif items == "Repository":
            return form_items(ReposForm, Repos)
        elif items == "Level":
            return form_items(LevelForm, Level)
        elif items == "Group":
            return form_items(GroupForm, Group)
    else:
        return render(request, 'index.html', {'log_out':True})
