'''
Created on May 12, 2009

@author: par
'''
from django.contrib.auth.models import User
from pollster.models import PollsterMessage, Poll
from django import forms
from django.forms.fields import CharField
from django.forms.widgets import Textarea, HiddenInput
from pollster.services.poll import PollService
from pollster.services.userservice import UserService
from pollster.views.base import base
from django.http import HttpResponseRedirect
from pollster.consts import consts


class MailUsersForm(forms.Form):
    subject = CharField(max_length=100)
    body = CharField(max_length=1500, widget=Textarea())

def mailusers(request):
    
    vars = {}
    form = None
    if request.method == 'POST': # If the form has been submitted...
        form = MailUsersForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            subject = form.cleaned_data["subject"]
            body = form.cleaned_data["body"]
            body = body.replace("\n", "<br/>")
            par_user = User.objects.get(username='par')
            # message every user in the system
            for u in User.objects.all():
                ps = PollService()
                ps.sendPollsterMessage(to_user=u, from_user=par_user, subject=subject, body=body)

            vars["done"] = True
    
    if not form:
        form = MailUsersForm(initial={"subject":"Recent updates"})
    vars["form"] = form
    return base.render(request, template="admin/mailuser.html", vars=vars)


