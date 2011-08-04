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

login('amir', 'amiradmin')
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
publication_xml = """
<publication xmlns="http://ht497.o1.gondor.io" xmlns:atom="http://www.w3.org/2005/atom"><abstract>        In computer science, functional programming is a programming paradigm that treats computation as the evaluation of mathematical functions and avoids state and mutable data. It emphasizes the application of functions, in contrast tothe imperative programming style, which emphasizes changes in state.[1] Functional programming has its roots in lambda calculus, a formal system developed in the 1930s to investigate function definition, function application, and recursion. Many functional programming languages can be viewed as elaborations on the lambda calculus.[1]    </abstract><address></address><booktitle></booktitle><chapter></chapter><doi>null</doi><edition></edition><editor></editor><howpublished></howpublished><institution></institution><isbn>212-45465-76768</isbn><journal></journal><number>12</number><organization></organization><pages></pages><publisher></publisher><review_status>1</review_status><publicationtype>ARTICLE</publicationtype><volume></volume><title>{The long tail: how endless choice is creating unlimited demand}</title><month></month><note></note><year>2012</year><owner><atom:link rel="user" type="application/xml" href="http://du865.o1.gondor.io/user/2"/></owner><ratings><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/16"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/17"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/18"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/19"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/21"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/22"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/23"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/24"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/25"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/26"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/27"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/28"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/29"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/30"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/31"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/32"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/33"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/34"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/35"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/36"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/37"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/38"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/39"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/40"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/41"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/42"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/43"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/44"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/45"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/46"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/47"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/48"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/1"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/49"/></rating><rating><atom:link rel="rating" type="application/xml" href="http://du865.o1.gondor.io/rating/20"/></rating></ratings><authors><author><atom:link rel="author" type="application/xml" href="http://du865.o1.gondor.io/author/1"/></author><author><atom:link rel="author" type="application/xml" href="http://du865.o1.gondor.io/author/2"/></author><author><atom:link rel="author" type="application/xml" href="http://du865.o1.gondor.io/author/3"/></author></authors><comments><comment><atom:link rel="comment" type="application/xml" href="http://du865.o1.gondor.io/comment/1"/></comment><comment><atom:link rel="comment" type="application/xml" href="http://du865.o1.gondor.io/comment/2"/></comment><comment><atom:link rel="comment" type="application/xml" href="http://du865.o1.gondor.io/comment/4"/></comment><comment><atom:link rel="comment" type="application/xml" href="http://du865.o1.gondor.io/comment/5"/></comment></comments><tags><tag><atom:link rel="tag" type="application/xml" href="http://du865.o1.gondor.io/tag/3"/></tag><tag><atom:link rel="tag" type="application/xml" href="http://du865.o1.gondor.io/tag/5"/></tag><tag><atom:link rel="tag" type="application/xml" href="http://du865.o1.gondor.io/tag/17"/></tag></tags><keywords><keyword><atom:link rel="keyword" type="application/xml" href="http://du865.o1.gondor.io/keyword/4"/></keyword><keyword><atom:link rel="keyword" type="application/xml" href="http://du865.o1.gondor.io/keyword/5"/></keyword><keyword><atom:link rel="keyword" type="application/xml" href="http://du865.o1.gondor.io/keyword/6"/></keyword><keyword><atom:link rel="keyword" type="application/xml" href="http://du865.o1.gondor.io/keyword/7"/></keyword><keyword><atom:link rel="keyword" type="application/xml" href="http://du865.o1.gondor.io/keyword/8"/></keyword><keyword><atom:link rel="keyword" type="application/xml" href="http://du865.o1.gondor.io/keyword/9"/></keyword><keyword><atom:link rel="keyword" type="application/xml" href="http://du865.o1.gondor.io/keyword/10"/></keyword><keyword><atom:link rel="keyword" type="application/xml" href="http://du865.o1.gondor.io/keyword/11"/></keyword><keyword><atom:link rel="keyword" type="application/xml" href="http://du865.o1.gondor.io/keyword/12"/></keyword><keyword><atom:link rel="keyword" type="application/xml" href="http://du865.o1.gondor.io/keyword/13"/></keyword><keyword><atom:link rel="keyword" type="application/xml" href="http://du865.o1.gondor.io/keyword/14"/></keyword><keyword><atom:link rel="keyword" type="application/xml" href="http://du865.o1.gondor.io/keyword/15"/></keyword></keywords><referencematerials><referencematerial><atom:link rel="referencematerial" type="application/xml" href="http://du865.o1.gondor.io/referencematerial/3"/></referencematerial><referencematerial><atom:link rel="referencematerial" type="application/xml" href="http://du865.o1.gondor.io/referencematerial/2"/></referencematerial><referencematerial><atom:link rel="referencematerial" type="application/xml" href="http://du865.o1.gondor.io/referencematerial/1"/></referencematerial></referencematerials><series></series></publication>
"""
put_resource(base_url + 'publication/1', publication_xml)
