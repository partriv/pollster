'''
Created on Mar 8, 2009

@author: par
'''
from pollster.views.base import base
from pollster.consts import consts
from django import forms
from django.forms.fields import CharField, EmailField
from django.forms.widgets import PasswordInput, TextInput
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from pollster.services.facebookservice import FacebookService
#from facebook.djangofb import Facebook
from pollster.services.userservice import UserService
from pollster.models import UserData
from django.contrib.auth.models import User
from pollster.conf import settings_local
import logging
import pollster.settings

class LoginForm(forms.Form):    
    username = CharField(max_length=30)
    password = CharField(widget=PasswordInput)

def login_block(request, next=None):
    vars = {}
    if next == None:
        next = request.GET.get("next", None)
    vars['form'] = LoginForm()
    vars['next'] = next
    return render_to_response('login_block.html', vars)

def index(request):    
    if request.user.is_authenticated():
        return HttpResponseRedirect("/profile/%s/" % request.user.username)

    next = request.GET.get("next", None)

    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST)
        if form.is_valid(): # All validation rules pass
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                # TODO: AYT #if user.is_active:
                auth.login(request, user)

                # get next redirect
                next = request.POST.get("next", None)
                if next == None or next == 'None':
                    return HttpResponseRedirect('/profile/%s/' % user.username) # Redirect after POST
                else:
                    return HttpResponseRedirect(str(next)) # Redirect after POST
            else:
                
                return base.render(request, "login.html", {"form":form, "errors":"Wrong username or password.  Can't log you in!",})
    else:
        form = LoginForm() # An unbound form

    return base.render(request, "login.html", {"form":form, "next":next})


def facebook_login(request):
    vars = {}
    log = logging.getLogger('facebook_login')
    #######
    # TODO: try to get facebook user info out of db here
    #######
    
    auth_token = request.GET.get("auth_token", None)
    fb = Facebook(settings.FACEBOOK_API_KEY, settings.FACEBOOK_SECRET_KEY)
    if not auth_token:
        return HttpResponseRedirect(fb.get_login_url(next=settings_local.HOST_NAME + "facebook-connect/"))
        

class FacebookConnectForm(forms.Form):
    username = CharField(min_length=2, max_length=30, 
                         help_text="30 characters or fewer. Alphanumeric characters only (letters, digits and underscores)", 
                         widget=TextInput(attrs={"onfocus":"showRegHelp('username');", "onblur":"hideRegHelp('username');return checkUsername();", "onkeyup":"return checkUsername();"}))
    email = EmailField()

def facebook_connect(request):
    next = request.GET.get("next", None)
    vars = {}
    form = FacebookConnectForm()
    vars["form"] = form
    
    log = logging.getLogger('facebook_connect')
    request.session['session_key'] = request.COOKIES.get(settings.FACEBOOK_API_KEY + '_session_key')
    request.session['uid'] = request.COOKIES.get(settings.FACEBOOK_API_KEY + '_uid')
    log.debug("session key: " + str(request.session['session_key'])) 
    log.debug("uid: " + str(request.session['uid'])) 
    fb = FacebookService().getFacebookSession(request)
    if not fb:
        log.critical("Facebook Service did not initialize")
        return HttpResponseRedirect(fb.get_login_url())
    
    vars["fb"] = fb    
    uid = fb.users.getLoggedInUser()
    uid = int(uid)
    log.debug("user id: " + str(uid))
        
    try:
        data = UserData.objects.get(facebook_id=uid)      #@UndefinedVariable
        # user already has facebook connected to an account
        # just log them in and redirect them        
        user = User.objects.get(id=data.user.id)
        log.debug("User already exists...")
        if not request.user.is_authenticated():
            user = auth.authenticate(username=user.username, password=FacebookService().getUserPassword(uid))
            try:            
                auth.login(request, user)
            except NotImplementedError:
                # user already had a pollstruck account with a diff password
                vars["login_block"] = True
                vars["no_facebook"] = True
                vars["form"] = LoginForm()
                return base.render(request=request, template="user/facebook_connect.html", vars=vars)            
        if next:
            return HttpResponseRedirect(next)
        return HttpResponseRedirect("/profile/%s/" % user.username)
    except UserData.DoesNotExist:      #@UndefinedVariable
        
        if request.user.is_authenticated() and request.user.userdata_set.get(user=request.user).facebook_id == None:
            log.debug("linking accounts")
            # user has pollstruck account already but no facebook
            # link their account to facebook automatically
            us = UserService(user=request.user)
            data = us.getUserData()
            data.facebook_id = uid 
            data.save()
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect('/profile/%s/' % request.user.username)
        
        
    # they are good to go
    if request.method == 'POST':
        form = FacebookConnectForm(request.POST)
        vars["form"] = form
        if form.is_valid():
            # create a user for the facebook user
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            if User.objects.filter(username=username).count() > 0:                
                vars["user_error"] = "That username exists"
                return base.render(request=request, template="user/facebook_connect.html", vars=vars)
            if User.objects.filter(email=email).count() > 0:
                vars["email_error"] = "That email exists"
                return base.render(request=request, template="user/facebook_connect.html", vars=vars)
                
            us = UserService()
            user = us.createUser(username=username, email=email, password=FacebookService().getUserPassword(uid))            
            auth.login(request, user)
            data = us.getUserData()
            data.facebook_id = uid
            # default all *new* incoming facebook users to use their facebook pic
            data.use_profile_pic = False 
            data.save()            
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect('/')
    else:
        pass

    return base.render(request=request, template="user/facebook_connect.html", vars=vars)
    


