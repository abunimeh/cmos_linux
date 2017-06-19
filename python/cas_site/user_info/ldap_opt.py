#Description: ldap3 API

from django.conf import settings
import ldap3
import random
import crypt
import string

#####global variables#####
server_url = settings.AUTH_LDAP_SERVER_URI
server_cn = settings.AUTH_LDAP_BIND_DN
server_passwd = settings.AUTH_LDAP_BIND_PASSWORD
sobj_cl = '(objectclass=person)'
mobj_cl = ['inetOrgPerson',
            'organizationalPerson',
            'person',
            'posixAccount',
            'top',
            'shadowAccount']
obj_gp = '(objectclass=posixGroup)'
attrs_user = ['displayName',
              'uidNumber',
              'uid',
              'mail', 
              'gidNumber', 
              'telephoneNumber', 
              'userPKCS12', 
              'manager', 
              'userPassword']
attrs_gp = ['cn','gidNumber', 'description']
search_gp = 'ou=Group,dc=sari,dc=com'


##### ldap user password coding#####    
def getsalt(chars = string.ascii_letters + string.digits):
    return random.choice(chars) + random.choice(chars)

##### ldap server connect#####    
def ldap3_connect(server = server_url, username = server_cn, passwd = server_passwd):
    s = ldap3.Server(server,get_info=ldap3.ALL)
    c_ins = ldap3.Connection(s,user = username, password = passwd, lazy = True)
    c_ins.bind()
    return c_ins

#####query ldap server return all user name <---> user id dict#####    
def ldap3_query_user(c_ins, search_base = settings.OU, search_filter = sobj_cl, attributes = attrs_user, allusers = False):
    c_ins.search(search_base=search_base,search_filter=search_filter,attributes=attributes)
    dict_user_id = {}
    if not allusers:
        for entry in c_ins.entries:
            if entry.entry_attributes_as_dict.get('userPKCS12',False) and \
                    (entry.entry_attributes_as_dict.get('userPKCS12')[0] == b'0'):
                dict_user_id[entry.uid.value]=[entry.uidNumber.value, 
                                               entry.gidNumber.value, 
                                               entry.manager.value]
    else:
        for entry in c_ins.entries:
            dict_user_id[entry.uid.value]=[entry.uidNumber.value, 
                                           entry.gidNumber.value,
                                            entry.manager.value]
    return dict_user_id

#####query ldap server return all group name <---> group id dict#####    
def ldap3_query_group(c_ins, search_base = search_gp,search_filter = obj_gp ,attributes = attrs_gp):
    c_ins.search(search_base=search_base,search_filter=search_filter,attributes=attributes)
    dict_group_id = {}
    for entry in c_ins.entries:
        if entry.entry_attributes_as_dict.get('description',False) and \
                entry.entry_attributes_as_dict.get('description')[0] == 'cpu':        
            dict_group_id[entry.cn.value]=entry.gidNumber.value
    return dict_group_id

def ldap3_modify(c_ins, userinfo, operation):
    userdn = 'uid=' + userinfo['username'] + ','+ settings.OU
    if operation == 'Edit':
        c_ins.modify(userdn, {'telephoneNumber':[(ldap3.MODIFY_REPLACE,userinfo['tel'])]})
    elif operation == 'Delete':
        c_ins.modify(userdn, {'userPKCS12':[(ldap3.MODIFY_REPLACE,userinfo['state'])]})
    elif operation == 'Passwd':
        salt = getsalt()
        reset_ps_crypt = '{crypt}' + crypt.crypt(userinfo['passwd'],salt)    
        c_ins.modify(userdn, {'userPassword':[(ldap3.MODIFY_REPLACE,reset_ps_crypt)]})            
    return ldap3_search_user(c_ins, userinfo['username'])

#####query ldap members based on username or leader or teamname  <---> group id dict#####    
def ldap3_search_membs(c_ins, utname, sg_memb = True, all_membs = False, attributes = attrs_user ):
    def entry_filter(user_entry):
        if (user_entry.entry_attributes_as_dict.get('userPKCS12',False) and
                user_entry.entry_attributes_as_dict.get('userPKCS12')[0] == b'0'):
            return True
    def user_info(user_entry, utname):
        userdic = {'username': user_entry.displayName.value, 
                   'email': user_entry.mail.value,
                   'team': utname,
                   'tel': user_entry.telephoneNumber.value,
                   'manager': user_entry.manager.value.split(',')[0].split('=')[1]} 
        return userdic
    userinfo = {utname :[]}
    dict_groud_id = ldap3_query_group(c_ins)
    c_ins.search(settings.OU , sobj_cl, attributes = attributes)
    if sg_memb: 
        userdn = 'uid='+ utname + ',' + settings.OU
    if not all_membs:
        if sg_memb: #search single members
            for user_entry in c_ins.entries:
                if (user_entry.manager.value == userdn and
                        entry_filter(user_entry)):
                    for  team, team_id in dict_groud_id.items():
                            if team_id == user_entry.gidNumber.value:
                                teamnm = team                    
                    userdic = user_info(user_entry, teamnm)
                    userinfo[utname].append(userdic)
        else: #search team members
            for user_entry in c_ins.entries:
                if (user_entry.gidNumber.value == dict_groud_id[utname] and 
                        entry_filter(user_entry)):
                    userdic = user_info(user_entry, utname)
                    userinfo[utname].append(userdic)        
    else: #search all members
        for user_entry in c_ins.entries: 
            if entry_filter(user_entry):
                for  team, team_id in dict_groud_id.items():
                    if team_id == user_entry.gidNumber.value:
                        teamnm = team                                        
                userdic = user_info(user_entry, teamnm)
                userinfo[utname].append(userdic)                              
    return userinfo

##### query login user information #####
def ldap3_search_user(c_ins, username):
    userinfo = {}
    c_ins.search('uid=' + username + ',' + settings.OU, sobj_cl, attributes = attrs_user)
    for entry_obj in c_ins.entries:
        userinfo['username'] =  entry_obj.displayName.value
        userinfo['email'] = entry_obj.mail.value
        userinfo['team'] = entry_obj.gidNumber.value
        userinfo['tel'] = entry_obj.telephoneNumber.value
        userinfo['manager'] =  entry_obj.manager.value.split(',')[0].split('=')[1]
    for  team, team_id in ldap3_query_group(c_ins).items():
            if team_id == userinfo['team']:
                userinfo['team'] = team   
    return userinfo

#####add new members to ldap #####
def ldaps_add_users(c_ins, newuser):
    salt = getsalt()
    ps_crypt = '{crypt}' + crypt.crypt(newuser['password'],salt)
    dict_user_id = ldap3_query_user(c_ins, allusers = True)
    uidnum =[] 
    for id in dict_user_id.values():
        uidnum.append(id[0])
    dict_groud_id = ldap3_query_group(c_ins)
    newuser['email'] = newuser['username'] + '@cpu.com.cn'
    newuser['gidnum'] = dict_groud_id[newuser['team']]
    newuser['uidnum'] = max(uidnum) + 1
    newuser['state'] = '0'.encode()
    newuser['manager'] = 'uid='+newuser['manager']+',' + settings.OU
    newuser['homedir'] = '/home/' + newuser['username'] 
    user_dn = 'uid='+newuser['username']+','+ settings.OU
    attributes={'cn':newuser['username'],
                'displayName':newuser['username'],
                'gecos':newuser['username'],
                'gidNumber':newuser['gidnum'],
                'givenName':newuser['username'],
                'homeDirectory':newuser['homedir'],
                'loginShell':'/bin/csh',
                'mail':newuser['email'],
                'manager':newuser['manager'],
                'shadowLastChange':'17015',
                'shadowMax':'99999',
                'shadowMin':'0',
                'shadowWarning':'7',
                'sn':newuser['username'],
                'telephoneNumber':newuser['tel'],
                'uid':newuser['username'],
                'uidNumber':newuser['uidnum'],
                'userPassword':ps_crypt,
                'userPKCS12':newuser['state']}
    c_ins.add(dn = user_dn, object_class = mobj_cl , attributes = attributes)
