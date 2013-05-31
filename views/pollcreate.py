'''
Created on Mar 8, 2009

@author: par
'''
from django.contrib.auth.decorators import login_required
from pollster.views.base import base
from django import forms
from django.forms.fields import CharField, FileField, URLField
from pollster.models import Poll, PollAnswer, PollFile, PollVote
from django.http import HttpResponseRedirect
from django.forms.widgets import TextInput, Textarea
from pollster.services.poll import PollService
from django.utils.datastructures import MultiValueDictKeyError
from pollster.consts import consts
from pollster.consts.consts import MAX_PICS_PER_POLL
from urlparse import urlparse
from django.forms.util import ValidationError
from pollster.utils.string import StringUtils
import logging
import re



class PollForm(forms.Form):
    question = CharField(max_length=75)
    
@login_required
def index(request):
    vars = {}
    inactive_polls = Poll.objects.filter(user=request.user, active=False)      #@UndefinedVariable
    if len(inactive_polls) > 0:
        vars["inactive_polls"] = inactive_polls 
    
    form = PollForm()
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid(): # All validation rules pass
            p = Poll()
            question = form.cleaned_data["question"]
            question = question.strip()
            q_url = PollService().get_next_url(question)            
            p.question = form.cleaned_data["question"]
            p.url = q_url            
            p.user = request.user
            p.total_votes = 0
            p.total_comments = 0
            p.save()
            

            return HttpResponseRedirect("/create-poll/answers/%s/" % q_url)
    vars["form"] = form
    return base.render(request, "pollcreate.html", vars)

class VideoTagField(CharField):
    """
    CharField that makes sure the video tag is actually a video tag
    and not some malicious javascript, etc.
    """
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        super(VideoTagField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        if value == "":
            return value
        tags_whitelist =['object', 'param', 'embed']
        ultimate_regexp = "(?i)<\/?\w+((\s+\w+(\s*=\s*(?:\".*?\"|'.*?'|[^'\">\s]+))?)+\s*|\s*)\/?>"
              
        matches = re.finditer(ultimate_regexp, value)
        valid = False
        for match in matches:
            # super hackey shitty string clean up method
            tag = str(match.group())
            if tag.startswith("</"):
                tag = tag[2:]
            elif tag.startswith("<"):
                tag = tag[1:]
            try:
                tag = tag[0:tag.index(' ')]
            except ValueError:
                pass
            tag = tag.strip(" ")
            tag = tag.strip("'")
            tag = tag.strip("</")
            tag = tag.strip("<")
            tag = tag.strip(">")
            if tags_whitelist.count(tag) == 0:
                raise ValidationError("Not an embedded video tag")
            valid = True
        if not valid:
            raise ValidationError("Not an embedded video tag")
        return value


class PollAnswerForm(forms.Form):    
    tag = CharField(max_length=30, widget=TextInput(attrs={"autocomplete":"off",}), required=False)
    description = CharField(max_length=400, widget=Textarea(attrs={"onkeyup":"return countChars();"}), required=False)
    link = URLField(max_length=250, required=False)


@login_required
def answers(request, poll_url=None, errors=None, form=None):
    """answers creation view"""    
    
    vars = {}
    ps = PollService()    
    log = logging.getLogger("POLL CREATE")
    
    # get the poll    
    p = Poll.objects.get(url=poll_url)       #@UndefinedVariable
    vars["poll"] = p    
    # make sure the user editing the poll is the creator
    if p.user != request.user:
        log.debug("User attempting to finish poll creator who did not create it: %s" % p.url)
        return HttpResponseRedirect("/")
    if p.active:
        vars["edit_mode"] = True
        votes = PollVote.objects.filter(poll=p).count()   #@UndefinedVariable
        vars["edit_active"]  = votes < consts.POLL_VOTES_BEFORE_PERMANENTLY_ACTIVE 

    
    # get the answers
    pa = PollAnswer.objects.filter(poll=p)   #@UndefinedVariable
    pa_len = len(pa)
    if  pa_len > 0:
        moreAnswers = pa_len - consts.MIN_ANSWERS_FOR_ACTIVE_POLL
        if moreAnswers < 0:
            vars["moreAnswers"] = moreAnswers         
        vars["answers"] = pa
        
    #load up tags    
    tags = p.tags.all()
    if len(tags) > 0:
        vars["tags"] = tags

    
    if form == None:
        form = PollAnswerForm()
    
    # set initial fields
    form.fields["description"].initial= p.description
    plink = p.link
    form.fields["link"].initial= plink
    if plink != None and plink.strip() != "":
        vars["link"] = plink
        vars["domain"] = urlparse(plink)[1]
    
            
    vars["form"] = form
    vars["allow_user_answers"] = p.allow_user_answers
    vars["errors"] = errors
            
    return base.render(request, "poll_create_answers.html", vars)

@login_required
def finish(request, poll_url):
    log = logging.getLogger("PollCreate")
    p = Poll.objects.get(url=poll_url)   #@UndefinedVariable
    
    # a lil security
    if p.user != request.user:
        return HttpResponseRedirect("/")
    type = ''
    if request.method == 'POST':
        form = PollAnswerForm(request.POST)
        if form.is_valid():
            type = request.POST.get("pollcreatehidden", '')
            
            # save link
            p.link = form.cleaned_data["link"]
            
            # save desc
            desc = form.cleaned_data["description"]
            if desc != None and desc != "":
                p.description = desc
            p.save()
        else:
            return answers(request, poll_url=poll_url, form=form)    
        
        # just saving the poll
        if type == 'save':
            return HttpResponseRedirect("/preview-poll/%s/" % p.url)    
        if type == 'savequit':
            return HttpResponseRedirect("/profile/%s/not-finished/" % request.user.username) 
        
    #finish the poll, verify answers, tags, make active and go
    if PollAnswer.objects.filter(poll=p).count() < consts.MIN_ANSWERS_FOR_ACTIVE_POLL:   #@UndefinedVariable
        return answers(request, poll_url, {"answer_error":"A poll must have at least two answers"})
    if p.tags.count() < consts.MIN_TAGS_FOR_ACTIVE_POLL:
        return answers(request, poll_url, {"tag_error":"A poll must have at least one tag"})
    
    if type != 'saveupdate':
        if p.active == False:
            p.active = True
        p.save()    
    return HttpResponseRedirect("/view-poll/%s/" % p.url)