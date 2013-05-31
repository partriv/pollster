'''
Created on Mar 8, 2009

@author: par
'''
from pollster.views.base import base
from pollster.models import Tag
from pollster.services.poll import PollService
from django import forms
from django.forms.fields import CharField, ChoiceField
from django.forms.widgets import TextInput, Select
from django.http import HttpResponse
from django.shortcuts import render_to_response
from pollster.utils.request import RequestUtils
from pollster.consts import consts

class SearchForm(forms.Form):
    searchbox = CharField(max_length=300, widget=TextInput(attrs={"onkeyup":"return searchHandler(event);"}))
    type = ChoiceField(choices=((0, "questions and descriptions"), (1, "tags")), required=True, widget=Select(attrs={"onchange":"return changeSearch();"}))
    

def index(request, search_terms=None, page_num=1, sort=None):
    initial = {"type":0}
    vars = {}
    vars["sort"] = sort
    if search_terms:
        ps = PollService()
        user = RequestUtils.getCurrentUser(request)
        prefix = "/search/%s" % search_terms
        vars["prefix"] = prefix
        polls = ps.searchPolls(search_terms, user, sort)
        paging_prefix = ps.addSortSuffix(prefix, sort)
        polls = ps.getPollsForLister(polls, request.user, page_num, page_link_prefix=paging_prefix)
        vars.update(polls)
        vars["search_terms"] = search_terms
    vars["form"] = SearchForm(initial=initial)
    vars["meta_desc"] = "Pollstruck search for %s." % search_terms    
    return base.render(request, "search.html", vars)

def index_sort_comments(request, search_terms, page_num=1):
    return index(request=request, search_terms=search_terms, page_num=page_num, sort=consts.SORT_TYPE_COMMENTS)
def index_sort_votes(request, search_terms, page_num=1):
    return index(request=request, search_terms=search_terms, page_num=page_num, sort=consts.SORT_TYPE_VOTES)
def index_sort_date(request, search_terms, page_num=1):
    return index(request=request, search_terms=search_terms, page_num=page_num, sort=consts.SORT_TYPE_DATE)


def doSearch(request, search_terms=None):
    if search_terms == None:
        return HttpResponse("Please enter something!")
    
    user = RequestUtils.getCurrentUser(request)
    polls = PollService().searchPolls(search_terms, user)
    
    return render_to_response("base/poll_lister.html", {"polls":polls})

def tag(request, tag_name=None, page_num=1, sort=None):
    """
    tag search page
    """
    vars= {}
    vars["sort"] = sort
    initial = {"type":1}
    if tag_name:
        vars["search_terms"] = tag_name
        vars["tag"] = tag_name
        tag_prefix = "/tag/%s" % tag_name
        vars["prefix"] = tag_prefix
        
        tags = []
        tag_names = tag_name.split(",")
        for t in tag_names:
            try:
                tags.append(Tag.objects.get(name=t.strip()))   #@UndefinedVariable
            except Tag.DoesNotExist:   #@UndefinedVariable
                pass
        if len(tags) > 0:
            ps = PollService()
            user = RequestUtils.getCurrentUser(request)
            polls = ps.searchPollsByTag(tag=tags, sort=sort)
            prefix = ps.addSortSuffix(tag_prefix, sort)
            spolls = PollService().getPollsForLister(polls, user, page_num=page_num, page_link_prefix=prefix)
            vars.update(spolls)
                
    vars["form"] = SearchForm(initial=initial)
    # special side bar for tag search view
    tags = Tag.objects.filter()[0:200]   #@UndefinedVariable
    vars["side_nav_top_title"] = "Tags"
    vars["tag_cloud"] = buildTagCloud(tags)    
    desc = "Pollstruck Tag search for: "
    for t in tag_names:
        desc  += t.strip()
    desc = desc.rstrip(", ")
    vars["meta_desc"] = desc
    return base.render(request, "search.html", vars)

def tag_sort_comments(request, tag_name, page_num=1):
    return tag(request=request, tag_name=tag_name, page_num=page_num, sort=consts.SORT_TYPE_COMMENTS)
def tag_sort_votes(request, tag_name, page_num=1):
    return tag(request=request, tag_name=tag_name, page_num=page_num, sort=consts.SORT_TYPE_VOTES)
def tag_sort_date(request, tag_name, page_num=1):
    return tag(request=request, tag_name=tag_name, page_num=page_num, sort=consts.SORT_TYPE_DATE)

def buildTagCloud(tags):
    max = 0
    min = 0
    newTuples = []
    
    for tag in tags:
        if max < tag.poll_count:
            max = tag.poll_count
        if min > tag.poll_count:
            min = tag.poll_count
    max = float(max)
    min = float(min)
    
    maxFontSize = 24
    minFontSize = 10
    for tag in tags:
        ratio = (tag.poll_count - min) / (max - min)
        fontSize = ratio * (maxFontSize - minFontSize) + minFontSize            
        newRefinement = (tag.name, fontSize)
        newTuples.append(newRefinement)
    return newTuples  
