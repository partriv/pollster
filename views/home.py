'''
Created on Mar 7, 2009

@author: par
'''
from pollster.views.base import base
from pollster.models import Poll
from pollster.services.poll import PollService
from django.http import HttpResponseRedirect, Http404
from pollster.services.userservice import UserService
import logging
import datetime

DEFAULT_SLICE = 150

def compare_by (fieldname):
    def compare_two_dicts (a, b):
        return cmp(a[fieldname], b[fieldname])
    return compare_two_dicts

def slug_time(request, slug, time_length, page_num=1):
    daysago = None
    time_link_prefix ="/" + time_length
    if time_length == '24h':    
        daysago = datetime.datetime.now() - datetime.timedelta(hours=24)
    elif time_length == '7d':
        daysago = datetime.datetime.now() - datetime.timedelta(days=7)
    elif time_length == '30d':
        daysago = datetime.datetime.now() - datetime.timedelta(days=30)
    elif time_length == '365d':
        daysago = datetime.datetime.now() - datetime.timedelta(days=365)
    elif time_length == 'all':
        daysago = -1
        time_link_prefix = '/all'
        
    return slug_handler(request, slug=slug, daysago=daysago, page_num=page_num, time_link_prefix=time_link_prefix)

def slug_handler(request, slug=None, daysago=None, page_num=1, time_link_prefix=""):    
    log = logging.getLogger('Home Slug Handler')
    polls = None
    pc = None
    page_link_prefix = ""
    
    
    # try it as some other things
    if slug == None:
        polls = Poll.objects.filter(active=1).order_by('-date_modified') #@UndefinedVariable
        selected = "recent"
        polls = apply_date_filter(polls, daysago)
    elif slug == 'popular':
        poll_sort = []
        polls = Poll.objects.filter(active=1) #@UndefinedVariable
        polls = apply_date_filter(polls, daysago)
        for p in polls:
            pop_index = p.total_votes + p.total_comments
            poll_sort.append({"poll":p, "popularity":pop_index})
        poll_sort.sort(compare_by('popularity'))
        poll_sort.reverse()
        polls = [ps["poll"] for ps in poll_sort]
        page_link_prefix = '/%s' % slug.lower()
        selected = slug
    elif slug == 'new':
        polls = Poll.objects.filter(active=1).order_by('-date_created') #@UndefinedVariable
        polls = apply_date_filter(polls, daysago)
        page_link_prefix = '/%s' % slug.lower()
        selected = slug
    elif slug == 'votedon':
        polls = Poll.objects.filter(active=1).order_by('-total_votes') #@UndefinedVariable
        polls = apply_date_filter(polls, daysago)
        page_link_prefix = '/%s' % slug.lower()
        selected = slug
    elif slug == 'commented':
        polls = Poll.objects.filter(active=1).order_by('-total_comments') #@UndefinedVariable
        polls = apply_date_filter(polls, daysago)
        page_link_prefix = '/%s' % slug.lower()
        selected = slug        
    elif slug == '24h':
        daysago = datetime.datetime.now() - datetime.timedelta(hours=24)
        polls = Poll.objects.filter(active=1).order_by('-date_modified') #@UndefinedVariable
        polls = apply_date_filter(polls, daysago)
        time_link_prefix = "/" + slug
        selected = "recent"
    elif slug == '7d':
        daysago = datetime.datetime.now() - datetime.timedelta(days=7)
        polls = Poll.objects.filter(active=1).order_by('-date_modified') #@UndefinedVariable
        polls = apply_date_filter(polls, daysago)
        time_link_prefix = "/" + slug
        selected = "recent"
    elif slug == '30d':
        daysago = datetime.datetime.now() - datetime.timedelta(days=30)
        polls = Poll.objects.filter(active=1).order_by('-date_modified') #@UndefinedVariable
        polls = apply_date_filter(polls, daysago)
        time_link_prefix = "/" + slug
        selected = "recent"
    elif slug == '365d':
        daysago = datetime.datetime.now() - datetime.timedelta(days=365)
        polls = Poll.objects.filter(active=1).order_by('-date_modified') #@UndefinedVariable
        polls = apply_date_filter(polls, daysago)
        time_link_prefix = "/" + slug
        selected = "recent"
    elif slug == 'all':
        daysago = -1                            
        polls = Poll.objects.filter(active=1).order_by('-date_modified') #@UndefinedVariable
        polls = apply_date_filter(polls, daysago)
        time_link_prefix = "/" + slug
        selected = "recent"
    
    if polls == None:
        # try to fall back on a poll url
        try:
            log.debug("Could not handle slug %s, falling back to view poll" % slug)
            poll = Poll.objects.get(url=slug)   #@UndefinedVariable
            return HttpResponseRedirect("/view-poll/%s/" % poll.url)
        except Poll.DoesNotExist:           #@UndefinedVariable
            log.debug("Could not handle slug %s, 404" % slug)
        raise Http404
    
    return index(request=request, selected=selected, db_polls = polls, page_num=page_num, page_link_prefix=page_link_prefix, time_link_prefix=time_link_prefix)

def apply_date_filter(polls, daysago):
    if daysago != None:
        if daysago != -1:
            polls = polls.filter(date_modified__gt=daysago)
    else:
        polls = polls[0:DEFAULT_SLICE]
    return polls
    

def index(request, selected='recent', db_polls = None, daysago=None, page_num=1, page_link_prefix="", time_link_prefix=""):
    # PollService().reconcileTagCount()
    # PollService().reconcilePollVoteCounts()
    # PollService().reconcileUntaggedPolls()
    # PollService().reconcilePollCommentsCount()
    # PollService().resizeAnswerColumn()
    print 'setting pw'
    #UserService().set_user_pw('ew', '8a7p9a0a')
    
    polls = PollService().getPollsForLister(db_polls, request.user, page_num, page_link_prefix + time_link_prefix)
    vars = {} 
    vars.update(polls) 
    if page_num > 1:
        vars['show_ad'] = True
    vars["selected"] = selected    
    vars["link_prefix"] = page_link_prefix
    vars["time_link_prefix"] = time_link_prefix
    
    return base.render(request, "home.html", vars)


