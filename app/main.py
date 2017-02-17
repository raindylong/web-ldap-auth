#!/usr/bin/env python
#-*- coding: utf-8 -*-

from bottle import Bottle, request, response

import os
import ldap
import base64
import hashlib

_LDAP_SCHEMA = {
    "passwd": "userPassword",
    "sn": "sn",
    "given_name": "givenName",
    "email": "mail",
}


class LdapAuth(object):
    def __init__(self,
                 host, mgr_cred, mgr_passwd, base, filter_template="cn=%s"):
        self.base = base
        self.filter_template = filter_template
        self.host = host
        self.mgr_cred = mgr_cred
        self.mgr_passwd = mgr_passwd
        self.search_keys = _LDAP_SCHEMA.values()
        self.pid = os.getpid()
        self.connect()

    def reset(self):
        self.pid = os.getpid()
        self.ldap.unbind()
        self.connect()

    # web fork
    def check_fork(self):
        if self.pid != os.getpid():
            self.reset()

    def connect(self):
        try:
            self.ldap = ldap.open(self.host)
            self.ldap.simple_bind_s(self.mgr_cred, self.mgr_passwd)
        except ldap.LDAPError, error_message:
            print "LDAP Connect Fail: %s" % error_message

    def get_user(self, user):
        self.check_fork()
        search_filter = self.filter_template % user
        try:
            query_set = self.ldap.search_s(
                self.base,
                ldap.SCOPE_SUBTREE,
                search_filter,
                self.search_keys
            )
        except ldap.LDAPError, error_message:
            print "LDAP Couldn't Connect: %s, try reconnect" % error_message
            self.connect()  # reconnect
            return

        try:
            dn, entry = query_set[0]
            user = LdapUser(user)
            for k in _LDAP_SCHEMA:
                ldap_key = _LDAP_SCHEMA[k]
                values = entry.get(ldap_key)
                if not values:
                    return
                value = values[0]
                setattr(user, k, value)
            return user
        except IndexError:
            pass

class LdapUser(object):
    def __init__(self, user):
        self.user = user
        self.passwd = None

    def auth(self, passwd):
        return self.encode_ldap_passwd(passwd) == self.passwd

    def encode_ldap_passwd(self, passwd):
        return '{MD5}' + \
            base64.encodestring(hashlib.md5(passwd).digest()).strip()

# modify the LDAP information by yourself
LA = LdapAuth(host="127.0.0.1",
              base="ou=user,ou=login,dc=AAA.COM",
              mgr_cred="cn=manager,dc=AAA.COM",
              mgr_passwd= "makelove")


application=Bottle()

@application.route('/ldap/auth_web', 'POST')  # ldap auth webpath
def auth():
    user = request.params.get("user")
    passwd = request.params.get("passwd")

    authx = LA.get_user(user)
    if not authx.auth(passwd):
        response.status = 203

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=3898, debug=True, reloader=True)
