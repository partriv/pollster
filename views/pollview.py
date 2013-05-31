'''
Created on Mar 8, 2009

@author: par
'''
from pollster.views.base import base
from pollster.consts import consts
from pollster.models import PollAnswer, Poll, PollVote, PollFile, PollWatch
from pollster.exception.pexception import PollsterException
from pollster.views.login import login_block
from django.http import HttpResponseRedirect, HttpResponse,\
    HttpResponseForbidden, Http404
from django import forms
from django.forms.forms import Form
from django.forms.fields import CharField


from django.shortcuts import render_to_response
from pollster.services.poll import PollService

from urlparse import urlparse
from pollster.services.userservice import UserService
from pollster.list.listitem import PollResultSpilloverListItem
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from pollster.conf import settings_local
from factory.chart_factory import GChartFactory
from django.utils import simplejson
import traceback
import logging


# ok so first we need profile picture - question
# images, urls, other things the poll is about
# graph
# vote on answer
# comments

# the form that gets created should be based on a poll_answer_style factory


# default
# radio buttons
# possibly text input with ajax + radio buttons

def poll_answer_style_factory(answer_style, poll, answers):
    
    if answer_style == consts.PREDEFINED_ANSWERS:
        choices = []
        spillover_choices = []
        for i in range(0, len(answers)):
            if i < consts.POLL_ANSWERS_MAGIC_THRESH:                                 
                choices.append((answers[i].answer.id, answers[i].answer.answer))
            else:
                spillover_choices.append((answers[i].answer.id, answers[i].answer.answer))    
        
        class AllRadioButtonsForm(forms.Form):
            answers = forms.ChoiceField(widget=forms.RadioSelect(attrs={"onclick":"return voteAnswer();"}), choices=choices, label="answers")
            spillover_answers = forms.ChoiceField(widget=forms.RadioSelect(attrs={"name":"answers"}), choices=spillover_choices, label="spillover")
        return AllRadioButtonsForm()
    
    raise PollsterException(__file__ + ' poll_answer_style_factory did not get a valid answer_style')


class AnswerForm(Form):
    new_answer = CharField(max_length=250)

def preview(request, poll_url=None):    
    return index(request, poll_url=poll_url, preview=True)

def index(request, poll_url=None, demographics=None, preview=False):
    """
    index handler
    """
    
    log = logging.getLogger("POLL VIEW")
    pollService = PollService()
    vars = {}
    vars['show_ad'] = True
    vars["pollview"] = True
    vars["preview"] = preview
    p = None
    random_poll = pollService.get_random_polls(1, request.user)
    if len(random_poll) > 0:        
        vars["random_poll"] = random_poll[0]
    if poll_url == None:        
        return HttpResponseRedirect("/view-poll/%s/" % random_poll.url)        
    else:       
        try:
            # get the poll and its tags                
            if preview:
                p = Poll.objects.get(url=poll_url) #@UndefinedVariable
                if request.user != p.user:
                    log.debug("User %s trying to preview poll he doesn't own, %s" % (request.user.username, p.url))
                    raise Http404
            else:
                p = Poll.objects.get(url=poll_url, active=True) #@UndefinedVariable
        except Poll.DoesNotExist: #@UndefinedVariable
            log.debug("Attempt to view poll which is not active or does not exist, trying to send to create, slug: %s" % poll_url)
            return HttpResponseRedirect("/create-poll/answers/%s/" % poll_url)    
    
    tags = p.tags.all()
    vars["tags"] = tags
    vars["poll"] = p
    if p.description and p.description != "":
        vars["poll_desc"] = p.description
    if p.link:
        vars["domain"] = urlparse(p.link)[1]
    
    if p.total_votes == 0:
        vars["noVotes"] = True
    
    
    # get the poll files
    pf = PollFile.objects.filter(poll=p) #@UndefinedVariable
    vars["pollFiles"] = pollService.get_poll_file_w_icons(pf)
    
    # check for content box
    if len(pf) > 0 or p.video_link or p.link:
        vars["showContentBox"] = True
    
    # do not show voting form if user has already voted
    form = None     

    results = pollService.get_poll_results(p, drop_zero_results=False)

    # user is logged in   
    if request.user.is_authenticated():
        # check to see if user is watching this
        us = UserService(request.user)
        data = us.getUserData() 
        if data.polls_watched.filter(poll=p).count() > 0:
            vars["watching"] = True
                
        if request.user == p.user:
            vars["creator"] = True
        
        # get the answer forms
        try:
            # check if user has voted
            poll_vote = PollVote.objects.get(poll=p, user=request.user) #@UndefinedVariable
            vars['your_answer'] = poll_vote.poll_answer.answer
        except PollVote.DoesNotExist: #@UndefinedVariable
            # they haven't so show them the answer form
            form = poll_answer_style_factory(consts.PREDEFINED_ANSWERS, p, results)
        except PollVote.MultipleObjectsReturned: #@UndefinedVariable
            # oh jesus, somehow they have multiple votes, log it and take their first one
            poll_vote = PollVote.objects.filter(poll=p, user=request.user)[0] #@UndefinedVariable
            logging.getLogger("PollView").critical("user has more than one vote for a poll id: %d and user: %s." % (p.id, request.user.username)) 
    else:
        form = poll_answer_style_factory(consts.PREDEFINED_ANSWERS, p, results)

    # open flash chart
    demographic_url_param = ''
    if demographics:
        demographic_url_param = demographics
    
    ansForm = AnswerForm()
    vars["answerForm"] = ansForm
    vars['form'] = form
    
    
    # poll display type
    chart_type = consts.DEFAULT_CHART_TYPE
    vars["link_in_new_window"] = True
    if request.user.is_authenticated():
        data = UserService(request.user).getUserData()
        vars["link_in_new_window"] = data.link_in_new_window
        chart_type = data.default_chart_type
    
    # get the gchart
    vars["chart_type"] = chart_type
    gcf = GChartFactory()
    res_w_votes = []
    res_wo_votes = []
    # grab only the results with votes to display on the chart
    for r in results:
        if r.votes > 0:
            res_w_votes.append(r)
        else:
            res_wo_votes.append(r)
    pchart = gcf.get_chart(res_w_votes)
    vars["gChart"] = pchart.get_url()
    vars["results"] = res_w_votes
    vars['results_wo_votes'] = res_wo_votes
    
    # create description tag:
    description = ""
    description += "Is it: "
    for i in range(0, len(vars["results"])):
        a = vars["results"][i]
        if isinstance(a.answer, PollAnswer):            
            description += a.answer.answer + ", "
            if i+1 == len(vars["results"]) - 1:
                description += "or "
    description = description.rstrip(", ")
    description += "?  "
    if p.description:
        description += p.description
    vars["meta_desc"] = description
    
    if p.link:
        vars['domain'] = urlparse(p.link)  
    return base.render(request, "pollview.html", vars)



def new_answer(request):
    """
    handles form requests to add a new answer
    """
    log = logging.getLogger('Pollview.new_answer')
    vars = {}
    pid = request.POST.get("pid", None)
    if pid == None:
        return HttpResponseRedirect("/")
    
    preview = request.POST.get('preview', None)
    if str(preview).strip().lower() == 'true':
        return HttpResponseRedirect('/preview-poll/%s/' % Poll.objects.get(id=pid).url) #@UndefinedVariable
    
    poll = Poll.objects.get(id=pid, active=True) #@UndefinedVariable
            
    if not poll.allow_user_answers:
        # poll does not allow this sort of behavior
        return HttpResponseRedirect("/view-poll/%s/" % poll.url)
    
    user = request.user
    if not user.is_authenticated():
        return HttpResponseRedirect("/login/?next=" + '/view-poll/%s/' % poll.url )
    
    # user has already voted they cant add anymore answers
    if PollVote.objects.filter(poll=poll, user=user).count() > 0: #@UndefinedVariable
        log.warning("already voted: %s" + user.username)
        return HttpResponseRedirect('/view-poll/%s/' % poll.url)
    
    if request.method == 'POST': # If the form has been submitted...
        form = AnswerForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            answer = form.cleaned_data["new_answer"]
            
            newAnswer = None
            try:
                # see if it exists
                newAnswer = PollAnswer.objects.get(answer=answer, poll=poll) #@UndefinedVariable
            except PollAnswer.DoesNotExist: #@UndefinedVariable
                newAnswer = None
            
            if newAnswer == None:
                # make answer
                newAnswer = PollAnswer()
                newAnswer.poll = poll
                newAnswer.answer = answer
                newAnswer.user = user
                newAnswer.save()
            
            # automatically cast vote for new answer
            PollVote(poll=poll, poll_answer=newAnswer, user=user).save()
            
            # increment total vote count
            poll.total_votes += 1
            poll.save()
            
            if poll.user != request.user and poll.user.userdata_set.all()[0].email_on_vote:
                send_voted_email(to_email=poll.user.email, from_user=user, poll=poll)
            
            return HttpResponseRedirect("/view-poll/%s/" % poll.url)
        else:
            return HttpResponseRedirect("/")
    return HttpResponseRedirect("/")
            

######################################
# AJAX HANDLERS BITCHES!
######################################
  ##         ######    ##     ##    ##  
 ## ##         ##     ## ##    ##  ## 
##   ##        ##    ##   ##    ####
##   ##        ##    ##   ##     ##
#######  ####  ##    #######    ####
##   ##   ##   ##    ##   ##   ##  ##
##   ##    #####     ##   ##  ##    ##
#######################################

def answer_suggest(request):
    """
    ajax answer suggestion for new answer box
    """
    answer = request.GET.get("q", None)
    pid = request.GET.get("id", None)
    poll = Poll.objects.get(id=pid) #@UndefinedVariable
    if answer.strip() != "":
        answers = PollAnswer.objects.filter(poll=poll, answer__icontains=answer)[0:50] #@UndefinedVariable
    return render_to_response("ajax/list_more_answers.html", {"answers":answers})

def get_voters(request):
    """
    ajax request handler to get  voters for an answer
    """
    aid = request.GET.get("aid", None)
    pid = request.GET.get("pid", None)
    poll_answer=PollAnswer.objects.get(id=aid) #@UndefinedVariable
    votes = PollVote.objects.filter(poll=Poll.objects.get(id=pid), poll_answer=poll_answer) #@UndefinedVariable
    users = []
    for v in votes:
        users.append(v.user)
    vars = {}
    vars["answer"] = poll_answer.answer
    vars["users"] =  users
    vars["votes"] = len(votes)
    return base.render(request, "ajax/pollview-voters.html", vars)

def get_spillover_answers(request):
    """
    ajax handler for spill over request
    """
    pid = request.GET.get("pid", None)
    poll = Poll.objects.get(id=pid) #@UndefinedVariable
    answers = PollService().get_poll_results(poll, drop_zero_results=False)
    vars = {}
    for a in answers:
        if a.__class__ == PollResultSpilloverListItem:            
            vars["answers"] = a.spill_over_list
    vars["poll"] = poll
    return base.render(request, "pollview/pollview-answer-lister.html", vars)

def answer_poll(request):
    """
    ajax poll voting request handler
    """
    log = logging.getLogger('Pollview.answer_poll')
    user = request.user
    answer_id = request.GET['answer_id']
    poll_id = request.GET['poll_id']

    poll = Poll.objects.get(id=poll_id, active=True) #@UndefinedVariable
    
    if not request.user.is_authenticated():
        next = '/view-poll/%s/' % poll.url
        return login_block(request, next)

    poll_answer = PollAnswer.objects.get(id=answer_id)    #@UndefinedVariable
    if PollVote.objects.filter(user=user, poll=poll).count() > 0: #@UndefinedVariable
        # RUH OH!
        log.critical("user trying to vote on poll which he has already voted on, user: %s, poll id: %d" % (user.username, poll.id))
        return HttpResponseForbidden("You have already voted on this!")

    # save
    PollVote(poll=poll, poll_answer=poll_answer, user=user).save()
    # increment vote count
    poll.total_votes += 1
    poll.save()
    vars = {}
    vars["your_answer"] = poll_answer.answer
    vars["poll"] = poll
    
    if poll.user != request.user and poll.user.userdata_set.all()[0].email_on_vote:
        send_voted_email(to_email=poll.user.email, from_user=user, poll=poll)

    pollresultslist = PollService().get_poll_results(poll, drop_zero_results=False)
    vars["results"] = pollresultslist
    # check if the last thing here is spillover list
    with_ans = []
    for res in pollresultslist:
        if res.votes > 0:
            with_ans.append(res)


    gcf = GChartFactory()
    chart = gcf.get_chart(with_ans)  
    resp = render_to_response("pollview-results.html", vars)
    hsh = {'pvr': resp.content, 'chart':chart.get_url()}
    return HttpResponse(simplejson.dumps(hsh), mimetype='application/json') 
  


def send_voted_email(to_email, from_user, poll):
    """
    send the 'someone voted on your poll email!!!!!
    """
    
    log = logging.getLogger('Pollview.send_voted_email')
    #if the person voting is not the creator, email the creator
    body = """Hello!
            <br/>It looks like %s has voted on your poll <a href="%s">%s</a>.  We just thought you'd like to know.
            <br/>
            Btw, you can turn this email off from your settings page.  The link is on your profile page.
            <br/>
            <br/>                
            Thanks!
            <br/>
            -Pollstruck""" % (from_user.username, settings_local.HOST_NAME + "view-poll/" + poll.url + "/", poll.question)
    
    subject = '%s has voted on your poll' % from_user.username  
    from_email, to = 'Pollstruck@gmail.com', to_email
    text_content = 'Hello!\nIt looks like %s has voted on your poll: %s.  Just thought you would like to know!\nBtw, you can turn this email off from your settings page.  The link is on your profile page.\n\nThanks!\n-Pollstruck' % (from_user.username, poll.question)
    html_content = body
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except:
        # swallow ALL EXCEPTIONS ALWAYS ALLOW THE VOTE TO GO THROUGH
        # THIS IS THE EXCEPTION BLACKHOLE
        log.error('Could not send email to %s.' % to_email)
        log.error(traceback.format_exc())
        
@login_required
def watch_poll(request):
    """
    ajax handler signs up users to watch a poll
    """    
    log = logging.getLogger('pollview.watch_poll')
    pid = request.GET.get("pid", None)
    type = request.GET.get("type", None)
    ps = PollService()
    if type == 'a':
        # add the poll to request users watch
        userdata = UserService(request.user).getUserData()
        poll = Poll.objects.get(id=pid, active=True) #@UndefinedVariable
        
        if PollWatch.objects.filter(user=request.user, poll=poll).count() == 0: #@UndefinedVariable
            pw = PollWatch()
            pw.poll = poll
            pw.user = request.user
            pw.save()
            userdata.polls_watched.add(pw)                
            userdata.save()
        else:        
            log.error("User trying to watch poll multiple times, user: %s" % request.user.username)
            return HttpResponse("Already watching!")
        
                
        if poll.user != request.user:
            # send message to poll creator
            # as long as you arent poll creator
            subject = "%s is watching your poll" % request.user.username
            body = "Hello.  This is just a note to let you know %s is watching your poll '%s'.  Thanks, The Mgmt." % (request.user.username, poll.question)
            ps.sendPollsterMessage(to_user=poll.user, from_user=request.user, subject=subject, body=body)
            
            
        
        return HttpResponse("You are watching this poll")
    elif type == 'd':
        userdata = UserService(user=request.user).getUserData()        
        poll = Poll.objects.get(id=pid) #@UndefinedVariable
        pw = PollWatch.objects.get(user=request.user, poll=poll) #@UndefinedVariable
        userdata.polls_watched.remove(pw)
        userdata.save()
        pw.delete()
        return HttpResponse("You are no longer watching this poll")
    
    return HttpResponseForbidden("unauthorized")

def flag_inappropriate(request):
    """
    ajax handler to flag inappropriate
    """
    
    pid = request.GET.get("pid")
    poll = Poll.objects.get(id=pid, active=True) #@UndefinedVariable
    poll.inappropriate = True
    poll.save()
    return HttpResponse(content="Thanks for helping, we'll take a look.")
    
    
def delete_comment(request):
    pass
    
    
    
    
    
    
    
    