import cookielib, urllib2
from urllib2 import HTTPError

#base_url = 'http://127.0.0.1:8000/'
base_url = 'http://du865.o1.gondor.io/'
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
#get_resource(base_url + 'publication/''application/xml')
#author_xml = """<?xml version="1.0" encoding="utf-8"?>
#<author xmlns="http://someurl/"
#    xmlns:atom="http://www.w3.org/2005/atom">
#    <name>
#        Jack
#    </name>
#    <address>
#        123 Funroad
#    </address>
#    <affiliation>
#        None
#    </affiliation>
#    <email>
#        None@none.none
#    </email>
#</author>"""
#post_resource(base_url + 'author/', author_xml, 'application/xml')
#
#rating_xml = """<?xml version="1.0" encoding="utf-8"?>
#<rating xmlns="http://test"
#    xmlns:atom="http://www.w3.org/2005/atom">
#    <publication>
#        <atom:link rel="publication" type="application/xml" href="http://test/publication/1"/>
#    </publication>
#    <rating>
#        5
#    </rating>
#</rating>"""
#put_resource(base_url + 'rating/1', rating_xml)

#data = file("entries.bib").read()
#post_resource(base_url + 'publication/', data, 'application/x-bibtex')
publication_xml = """<publication xmlns="http://du865.o1.gondor.io" xmlns:atom="http://www.w3.org/2005/atom">
<abstract></abstract>
<address>None</address>
<booktitle>None</booktitle>
<chapter>None</chapter>
<doi>10.1038/nature04992</doi>
<edition>None</edition>
<editor>None</editor>
<howpublished></howpublished>
<institution>None</institution>
<isbn>None</isbn>
<journal>Nature</journal>
<number>None</number>
<organization>None</organization>
<pages>None</pages>
<publisher>None</publisher>
<review_status>1</review_status>
<series>None</series>
<publicationtype>ARTICLE</publicationtype>
<volume>None</volume>
<title>Wisdom of the crowds</title>
<month>None</month>
<note>None</note>
<year>2006</year>
<ratings></ratings>
<owner>
<atom:link rel="owner" type="application/xml" href="http://du865.o1.gondor.io/user/3"/>
</owner>
<authors>
<author>
<atom:link rel="author" type="application/xml" href="http://du865.o1.gondor.io/author/2"/>
</author>
</authors>
<comments>
<comment>
<atom:link rel="comment" type="application/xml" href="http://du865.o1.gondor.io/comment/1"/>
</comment>
</comments>
<tags></tags>
<keywords></keywords>
<referencematerials></referencematerials>
<fields></fields>
</publication>"""
put_resource(base_url + 'publication/54', publication_xml)
