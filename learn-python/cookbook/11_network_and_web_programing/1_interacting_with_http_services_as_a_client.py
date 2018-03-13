#!/usr/bin/python3
# coding utf8
from urllib import request, parse
# Base URL being accessed
url = 'http://httpbin.org/get'

# dictionary of query parameters
parms = {
    'name1': 'value1',
    'name2': 'value2'
}

# encode the query string
querystring = parse.urlencode(parms)

# make a GET request and read the response
u = request.urlopen(url + '?' + querystring)
res = u.read()

"""
if you need send the query parameters in the request body using a POST method,
encode them and supply them as an optional argument to urlopen() like this:
"""
url = 'http://httpbin.org/post'
parms = {
    'name1': 'value1',
    'name2': 'value2'
}
querystring = parse.urlencode(parms)
# make a POST request and read the response
u = request.urlopen(url, querystring.encode('ascii'))
res = u.read()

"""
If you need to supply some custom HTTP headers in the outgoing request such as
a change to the user-agent field, make a dictionary containing their value and create a Request
instance and pass it to urlopen() like this:
"""
headers = {
    'User-agent': 'xxxxxx/xxxxx',
    'Spam': 'eggs'
}
req = request.Request(url, querystring.encode('ascii'), headers=headers)
# make a request and read the response
u = request.urlopen(req)
res = u.read()

