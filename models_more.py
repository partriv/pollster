'''
Created on May 11, 2009

@author: par
'''

from django.db import models
from pollster.models import Poll, Tag, UserData, PollWatch

class Poll_Tags(models.Model):
    poll = models.ForeignKey(Poll)
    tag = models.ForeignKey(Tag)
    
class UserData_Polls_Watched(models.Model):
    userdata = models.ForeignKey(UserData)
    pollwatch = models.ForeignKey(PollWatch)
    
