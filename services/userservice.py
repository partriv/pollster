'''
Created on Apr 11, 2009

@author: par
'''
from pollster.models import UserData
from pollster.utils.file import FileUtils
from pollster.conf import settings_local
from pollster.consts import consts
from django.contrib.auth.models import User
from pollster.exception.pexception import PollsterException
from django.contrib import auth

class UserService():
    
    __user = None
    __data = None
    
    def __init__(self, user=None):
        self.__user = user
    
    def createUser(self, username=None, email=None, password=None):
        # register the user
        if not (username and email and password):
            raise PollsterException("User not created, not enough params")

        username = username.strip()
        User.objects.create_user(username, email, password)
        user = auth.authenticate(username=username, password=password)
        # initialize user data so they get profile pic, etc.
        UserService(user=user).getUserData()
        self.__user = user            
        return user
            
         
    def getUserData(self):        
        if self.__data == None:
            # caching
            data = None
            try:
                data = UserData.objects.get(user=self.__user)   #@UndefinedVariable
            except UserData.DoesNotExist:   #@UndefinedVariable
                newData = UserData()
                newData.user = self.__user
                newData.save()
                return newData
            self.__data = data        
        return self.__data
    
    def getPollsWatched(self):
        polls = []
        for pw in self.getUserData().polls_watched.all():
            polls.append(pw.poll)
        return polls
            
    def uploadUserPic(self, file):
        thumbs = [(settings_local.USER_FILES_THUMBS_TINY, consts.THUMB_WIDTH_TINY, consts.THUMB_HEIGHT_TINY),
                  (settings_local.USER_FILES_THUMBS_SMALL, consts.THUMB_WIDTH_SM, consts.THUMB_HEIGHT_SM),
                  (settings_local.USER_FILES_THUMBS_MEDIUM, consts.THUMB_WIDTH_MED, consts.THUMB_HEIGHT_MED),
                  (settings_local.USER_FILES_THUMBS_BIG, consts.THUMB_WIDTH_LG, consts.THUMB_HEIGHT_LG)]
        name = FileUtils.uploadFile(file, upload_path=settings_local.UPLOAD_USER_PIC_PATH, thumbnails=thumbs)
        if name:
            data = self.getUserData()
            data.profile_pic = name
            data.save()
            self.__data = data
            return name
        else:
            return None
    
    def getFriends(self):
        data = self.getUserData()
        friends = data.friends.select_related().all()
        return friends
    
    def getFriend(self, user):
        data  = self.getUserData()
        try:
            friend = data.friends.get(username=user.username)
        except User.DoesNotExist:   #@UndefinedVariable
            return None
        return friend
    
    def set_user_pw(self, username, pw):
        u = User.objects.get(username=username)
        u.set_password(pw)
        u.save()