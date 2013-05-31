'''
Created on May 21, 2009

@author: par
'''
from django import template
from django.contrib.auth.models import User
from pollster.services.userservice import UserService
from pollster.conf import settings_local

register = template.Library()

@register.filter
def get_user_pic(id, size):
    u = User.objects.get(id=id)
    data = UserService(user=u).getUserData()
    if data.facebook_id and (not data.use_profile_pic):
            if size == 'big':
                return '<fb:profile-pic uid="' + str(data.facebook_id) + '" linked="false" facebook-logo="true" size="normal" height="128"></fb:profile-pic>'
            elif size == 'medium':
                return '<fb:profile-pic uid="' + str(data.facebook_id) + '" linked="false" facebook-logo="true" size="small" height="64"></fb:profile-pic>'
            elif size == 'small':
                return '<fb:profile-pic uid="' + str(data.facebook_id) + '" linked="false" facebook-logo="true" size="small" height="24"></fb:profile-pic>'
            else:
                return '<fb:profile-pic uid="' + str(data.facebook_id) + '" linked="false" facebook-logo="true" size="tiny" height="16"></fb:profile-pic>'
    else:
        if size == "big":
            return '<img alt="' + u.username + '" src="' + settings_local.USER_FILES_URL + settings_local.USER_FILES_THUMBS_BIG + data.profile_pic + '" />'
        elif size == "medium":
            return '<img alt="' + u.username + '" src="' + settings_local.USER_FILES_URL + settings_local.USER_FILES_THUMBS_MEDIUM + data.profile_pic + '" />'
        elif size == "small":
            return '<img alt="' + u.username + '" src="' + settings_local.USER_FILES_URL + settings_local.USER_FILES_THUMBS_SMALL + data.profile_pic + '" />'
        else:
            return '<img alt="' + u.username + '" src="' + settings_local.USER_FILES_URL + settings_local.USER_FILES_THUMBS_TINY + data.profile_pic + '" />'
    