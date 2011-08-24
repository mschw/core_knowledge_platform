import cookielib, urllib2
from urllib2 import HTTPError
import timeit
import time

base_url = 'http://127.0.0.1:8000/'
#base_url = 'http://192.168.56.101/'
#base_url = 'http://du865.o1.gondor.io/'
cookies = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
headers = [('accept', 'application/xml'), ('content-type', 'application/xml'),]
opener.addheaders = headers

def print_response(response):
    """Print a response"""
    #for key, header in response.getheaders():
    #    print "%s: %s" % (key, header)
    print "%s" % (response.headers)
    print response.read()

def login(username, password):
    """log a client in."""
    login_xml = """<?xml version="1.0" encoding="utf-8"?>
    <login xmlns:atom="http://www.w3.org/2005/atom">
        <username>%s</username>
        <password>%s</password>
        <user>
            <atom:link rel='user' type='application/xml' href='%s/user/0'/>
        </user>
    </login>""" % (username, password, base_url)
    url = base_url + 'user/login/'
    try:
        response = opener.open(url, login_xml)
        print_response(response)
    except HTTPError, e:
        print "Error: %s\n%s" % (e, e.read())

def post_resource(url, xml, content_type):
    try:
        request = urllib2.Request(url=url, data=xml)
        request.add_header(key='content-type', val=content_type)
        response = opener.open(request)
        print_response(response)
    except HTTPError, e:
        print "Error: %s\n%s" % (e, e.read())

def put_resource(url, xml):
    try:
        request = urllib2.Request(url=url, data=xml)
        request.add_header(key='content-type', val='application/xml')
        request.get_method = lambda: 'PUT'
        response = opener.open(request)
        print_response(response)
    except HTTPError, e:
        print "Error: %s\n%s" % (e, e.read())

def delete_resource(url, xml):
    """docstring for delete_resource"""
    pass

def get_resource(url):
    response = opener.open(url)
    print_response(response)

login('testuser', 'django')

data = file("entries.bib").read()
post_resource(base_url + 'publication/', data, 'application/x-bibtex')
