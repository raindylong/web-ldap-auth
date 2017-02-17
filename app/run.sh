#!/bin/bash

#/usr/local/bin/uwsgi -s /tmp/uwsgi.web-ldap-auth.sock -M -c -p1 --enable-threads --chmod-socket=666 -L --listen=256 \
#    --pidfile=./web-ldap-auth.pid --module=main --lazy-app

nohup /usr/local/bin/uwsgi --ini ./web_ldap_auth.ini --thunder-lock &
echo "web-ldap-auth start ..."

