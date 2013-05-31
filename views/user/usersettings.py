'''
Created on Apr 11, 2009

@author: par
'''
from pollster.views.base import base
from django.contrib import auth
from django.http import HttpResponseForbidden, HttpResponseNotFound,\
    HttpResponse
from pollster.models import UserData
from pollster.consts import consts
from django.contrib.auth.models import User
from pollster.services.userservice import UserService


def index(request, username):
    user = auth.models.User.objects.get(username = username)
    if request.user != user:
        return HttpResponseNotFound()
    
    data = UserData.objects.get(user=request.user)      #@UndefinedVariable
    
    vars = {}    
    vars["data"] = data
    vars["chart_type"] = data.default_chart_type 
    return base.render(request, "user/usersettings.html", vars)

def update_settings(request):
    type = request.GET.get("type", None)
    if not type:
        return HttpResponse(content="error 105")
    
    if type == '100':
        # update user chart
        return set_chart_type(request)
    elif type == '101':
        # update new window for link
        return link_new_window(request)
    elif type == '102':
        # email on vote
        return email_on_vote(request)
    elif type == '103':
        # email on poll comment
        return email_on_poll_comment(request)
    elif type == '104':
        # email on vote
        return email_on_comment_reply(request)        
    elif type == '200':
        # update setting to use profile pic or facebook pic
        return which_pic(request)
    else:
        return HttpResponse(content="error 106")
        

def set_chart_type(request):
    chart_type = request.GET.get("val", None)
    if not consts.CHART_TYPES_WHITE_LIST.count(chart_type):
        return HttpResponse(content="Not Saved")
    user = request.user
    
    data = UserService(user=user).getUserData()
    data.default_chart_type = chart_type
    data.save()
    return HttpResponse(content="Saved your selection: %s" % chart_type)

def link_new_window(request):
    user = request.user
    val = int(request.GET.get("val", None))
    val = val == 1

    data = UserService(user=user).getUserData()
    data.link_in_new_window = val
    data.save()
    if val:
        result = "Open in new window"
    else:
        result = "Open in same window"    
    return HttpResponse(content="Saved your selection: %s" % result)
    
def email_on_vote(request):
    user = request.user
    val = int(request.GET.get("val", None))
    val = val == 1

    data = UserService(user=user).getUserData()
    data.email_on_vote = val
    data.save()
    if val:
        result = "You will get an email when someone votes on your poll"
    else:
        result = "You won't receieve an email when someone votes on your poll"    
    return HttpResponse(content="Saved your selection: %s" % result) 

def which_pic(request):
    val = int(request.GET.get("val", None))
    val = val == 1    
    data = UserService(user=request.user).getUserData()
    data.use_profile_pic = val
    data.save()    
    if val:
        result = "Pollstruck pic"
    else:
        result = "Facebook pic"
    return HttpResponse(content="Saved your selection: %s" % result)

def email_on_poll_comment(request):
    user = request.user
    val = int(request.GET.get("val", None))
    val = val == 1

    data = UserService(user=user).getUserData()
    data.email_on_poll_comment = val
    data.save()
    if val:
        result = "You will get an email when someone comments on your poll"
    else:
        result = "You won't receieve an email when someone comments on your poll"    
    return HttpResponse(content=result)

def email_on_comment_reply(request):
    user = request.user
    val = int(request.GET.get("val", None))
    val = val == 1

    data = UserService(user=user).getUserData()
    data.email_on_comment_reply = val
    data.save()
    if val:
        result = "You will get an email when someone replies to your comment on a poll"
    else:
        result = "You won't get an email when someone replies to your comment on a poll"    
    return HttpResponse(content=result)     