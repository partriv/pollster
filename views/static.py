'''
Created on Mar 8, 2009

@author: par
'''
from pollster.views.base import base
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from pollster.conf import settings_local

def contact(request):
    return base.render(request, "static/contact.html")


def about(request):
    return base.render(request, "static/about.html")

def robots(request):
    response = HttpResponse(content_type="text/plain")
    f = open(settings_local.MEDIA_ROOT + "robots.txt")    
    response.content = f.read()
    f.close()
    return response

def sitemap(request):
    response = HttpResponse(content_type="text/xml")
    f = open(settings_local.MEDIA_ROOT + "sitemap.xml")    
    response.content = f.read()
    f.close()
    return response

def xd_receiver(request):
    response = HttpResponse()
    f = open(settings_local.MEDIA_ROOT + "xd_receiver.htm")    
    response.content = f.read()
    f.close()
    return response

def delorie(request):
    return HttpResponse()

def favicon(request):
    raise Http404
        