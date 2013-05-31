'''
Created on May 25, 2009

@author: par
'''
from pollster.models import Poll
from django.shortcuts import render_to_response
from pollster.views.base import base
import datetime


def get_vars():
    date = datetime.datetime.now().__str__()[:10]
    urls = []
    

    polls = Poll.objects.filter(active=True)      #@UndefinedVariable
    for p in polls:
        url = "http://www.pollstruck.com/view-poll/%s/" % (p.url)
        urls.append((p.question, url))
    vars = {}
    vars["urls"] = urls
    vars['date'] = date
    return vars

def sitemap(request):
    vars = get_vars()
    return base.render(request=request, template="sitemap.html", vars=vars)



def index(request):
    vars = get_vars()
    resp = render_to_response('sitemap.xml', vars,  mimetype="application/xhtml+xml")
    resp.mimetype = 'text/xml'
    return resp
        
    