# web-ldap-auth
verify ldap auth through web


(1) Install all necessary python module.

(2) Modify the LDAP information in main.py.

(3) Config your Nginx by the example nginx_auth.conf.

(4) Test case:

<code>
<pre>
test:~> curl --head -X POST 'http://127.0.0.1:3898/ldap/auth_web?user=test&passwd=1234'
HTTP/1.1 200 OK
Server: nginx/1.11.5
Date: Fri, 17 Feb 2017 03:38:01 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 0
Connection: keep-alive
Status: 200 OK

test:~> curl --head -X POST 'http://127.0.0.1:3898/ldap/auth_web?user=test&passwd=1233'
HTTP/1.1 203 Non-Authoritative Information
Server: nginx/1.11.5
Date: Fri, 17 Feb 2017 03:39:12 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 0
Connection: keep-alive
Status: 203 Non-Authoritative Information
</pre>
</code>


