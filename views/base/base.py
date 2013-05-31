'''
Created on Mar 7, 2009

@author: par
'''
from django.shortcuts import render_to_response
from pollster.models import Tag, Poll, PollsterMessage
from pollster.conf import settings_local
from pollster.utils.string import StringUtils
from pollster.services.poll import PollService
from pollster.services.userservice import UserService
from pollster.consts import consts
from pollster.factory import adfactory
from pollster import settings


import pollster.settings
import datetime


def render(request, template, vars=None):
    baseVars = {}
    baseVars["debug"] = settings.DEBUG
    baseVars["FACEBOOK_API_KEY"] = settings.FACEBOOK_API_KEY
    baseVars["FACEBOOK_SECRET_KEY"] = settings.FACEBOOK_SECRET_KEY
    
    baseVars["USER_FILES_URL"] = StringUtils.addTrailingSlash(settings_local.USER_FILES_URL)
    baseVars["USER_FILES_THUMBS_BIG"] = StringUtils.addTrailingSlash(settings_local.USER_FILES_THUMBS_BIG)
    baseVars["USER_FILES_THUMBS_MEDIUM"] = StringUtils.addTrailingSlash(settings_local.USER_FILES_THUMBS_MEDIUM)
    baseVars["USER_FILES_THUMBS_SMALL"] = StringUtils.addTrailingSlash(settings_local.USER_FILES_THUMBS_SMALL)
    baseVars["USER_FILES_THUMBS_TINY"] = StringUtils.addTrailingSlash(settings_local.USER_FILES_THUMBS_TINY)
    
    baseVars["POLL_FILES_URL"] = StringUtils.addTrailingSlash(settings_local.POLL_FILES_URL)
    baseVars["POLL_RESULTS_MAGIC_THRESH"] = consts.POLL_RESULTS_MAGIC_THRESH
    baseVars["SITE_NAME"] = consts.SITE_NAME
    baseVars["leader_board_ad"] = adfactory.get_leaderboard()
    baseVars["med_square_ad"] = adfactory.get_medium_square()
    
    
    baseVars["POLL_VOTES_BEFORE_PERMANENTLY_ACTIVE"] = consts.POLL_VOTES_BEFORE_PERMANENTLY_ACTIVE
     
    tags = Tag.objects.filter().order_by('-poll_count')[:100]   #@UndefinedVariable
    baseVars["header_tags"] = tags
    if request.user.is_authenticated():
        user = request.user    
        baseVars["user"] = user
        us = UserService(user)
        data = us.getUserData()
        msgCount = PollsterMessage.objects.filter(read=False, to_user=request.user).count()   #@UndefinedVariable
        baseVars["newMail"] = msgCount > 0
        baseVars["newMailCnt"] = msgCount
        baseVars["profile_pic"] = data.profile_pic
        
    
    
     
    # if conflict between child class and base class vars then child wins
    # so child can override base vars
    if vars:
        baseVars.update(vars)    
    return render_to_response(template, baseVars)


