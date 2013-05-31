'''
Created on Mar 8, 2009

@author: par
'''
from pollster.models import Poll, PollAnswer, Tag, UserProfile,\
    PollFile, PollVote
from pollster.views.profile import UserProfileDemoFilterForm
from django.http import HttpResponse, HttpResponseForbidden,\
    HttpResponseNotFound
from django.shortcuts import render_to_response
from django import forms
from threadedcomments.models import ThreadedComment
from pollster.conf import settings_local
from threadedcomments import views
from pollster.consts import consts
from django.core.mail import EmailMultiAlternatives
from pollster.services.userservice import UserService
import logging
import copy


##############################
# SEARCH AJAX
###############################

def search(request):
    text = request.GET.get("text", None)
    if text:
        questions = Poll.objects.filter(question__startswith=text, active=True)[:25]   #@UndefinedVariable
        return render_to_response("ajax/existing_polls_search_ajax.html", {"polls":questions, "len":len(questions)})
    else:
        return render_to_response("ajax/existing_polls_search_ajax.html")


# search tags at poll creator
def search_tags(request):
    tag = request.GET.get("q", None)
    tag_arr = tag.split(',')
    tag = tag_arr[len(tag_arr)-1]
    tags = None
    tag = tag.strip() 
    if tag != "":
        tags = Tag.objects.filter(name__icontains=tag).order_by('-poll_count')   #@UndefinedVariable
    return render_to_response("ajax/list_tags.html", {"tags":tags})   #@UndefinedVariable

# i need to get all tags that are attached to education
# need to get list of tags that are associated with education
# need to get a list of tags
# Tag.userprofile_set_education.all()
def search_profile_tags(request, field, many_to_many):
    tag = request.GET.get("q", None)
    limit = request.GET.get("limit", 10)
    tags = None
    if tag.strip() != "":
        user = UserProfile()
        tags = user.get_tags_like(tag, field, limit, int(many_to_many))

        if tags:
            tags = [tag[0] for tag in tags]

    return render_to_response("ajax/list_profile_tags.html", {"tags":tags})

##############################
# POLL CREATOR AJAX
###############################

def edit_title(request):
    if request.method == 'POST':
        pid = request.POST.get("pid", None)
        new_title = request.POST.get("new_title", None)
        # cant change question of active polls
        poll = Poll.objects.get(id=pid, active=False)   #@UndefinedVariable
        poll.question = new_title
        poll.save()

        return HttpResponse(content=poll.question)
    else:
        return HttpResponseNotFound()

def get_inactive(request):
    """
    not in use currently
    """
    
    inactive_polls = Poll.objects.filter(user=request.user, active=False)   #@UndefinedVariable
    return render_to_response("ajax/inactive_polls_search_ajax.html", {"polls":inactive_polls, "len":len(inactive_polls)})

def set_main_file(request, poll_id, poll_file_id):
    poll = Poll.objects.get(id=poll_id)   #@UndefinedVariable
    if request.user != poll.user:
        return HttpResponseForbidden("unauthorized")
    
    pollfiles = poll.pollfile_set.all()
    for pf in pollfiles:
        if pf.id == poll_file_id:
            pf.main_file = 1
        else:
            pf.main_file = 0
        pf.save()
    
    pf = PollFile.objects.get(id=poll_file_id)   #@UndefinedVariable
    pf.main_file = True
    pf.save()

    return HttpResponse("Done")


def delete_file(request, poll_id, poll_file_id):
    poll = Poll.objects.get(id=poll_id)   #@UndefinedVariable
    if request.user != poll.user:
        return HttpResponseForbidden("unauthorized")
    
    pf = poll.pollfile_set.get(id=poll_file_id)
    pf.delete()
    
    return HttpResponse("Done")

def reload_files(request, poll_id):
    p = Poll.objects.get(id=poll_id)   #@UndefinedVariable
    pf = p.pollfile_set.all()
    vars = {}
    vars["POLL_FILES_URL"] = settings_local.POLL_FILES_URL
    vars["pollFiles"] = pf
    vars["poll"] = p
    return render_to_response("poll-create-file-block.html", vars)
    

# add answer at poll creator
def add_answer(request):
    id = request.GET.get("id", None)
    answer = request.GET.get("a", None)
    
    # cant modify active polls
    p = Poll.objects.get(id=id, active=False)   #@UndefinedVariable
    # make sure user owns polls
    if p.user != request.user:
        return HttpResponseForbidden("unauthorized")

    vars = {}
    if answer.strip() != "":
        if PollAnswer.objects.filter(poll=p, answer=answer).count() < 1:   #@UndefinedVariable
            pa = PollAnswer()
            pa.poll = p
            pa.answer = answer
            pa.user = request.user
            pa.save()
        else:
            vars["dupe"] = True
    else:
        vars["whitespace"] = True
    
    vars["answers"] = PollAnswer.objects.filter(poll=p)   #@UndefinedVariable
    return render_to_response("ajax/poll_answers.html", vars)

# add answer at poll creator
def delete_answer(request):
    """
    delete an answer from the poll creator
    """
    
    id = request.GET.get("id", None)
    pa = PollAnswer.objects.get(id=id)   #@UndefinedVariable
    # cant modify active polls
    p = Poll.objects.get(id=pa.poll.id, active=False)   #@UndefinedVariable
    # make sure user owns polls
    if p.user != request.user:
        return HttpResponseForbidden("unauthorized")

    pa.delete()
    vars = {}
    vars["answers"] = PollAnswer.objects.filter(poll=p)   #@UndefinedVariable
    return render_to_response("ajax/poll_answers.html", vars)

# add tag at poll creator
def add_tag(request):
    id = request.GET.get("id", None)
    tag_name = request.GET.get("t", None)
    
    p = Poll.objects.get(id=id)   #@UndefinedVariable
    # make sure user owns polls
    if p.user != request.user:
        return HttpResponseForbidden("unauthorized")
    
    # get existing poll tags
    tags = p.tags.all()
    vars = {}
    vars["tags"] = tags
    tag_name = tag_name.strip()
    if tag_name == "":
        vars["error"] = "Please provide a valid tag"
        return render_to_response("ajax/list_poll_tags.html", vars)
    tag_names = tag_name.split(",")
    for tag_name in tag_names:
        tag_name = tag_name.strip()
        try:    
            tag = Tag.objects.get(name=tag_name)   #@UndefinedVariable
        except Tag.DoesNotExist:   #@UndefinedVariable
            tag = Tag()
            tag.name = tag_name
        
        #increment the count
        if tag.poll_count:
            tag.poll_count += 1
        else:
            tag.poll_count = 1
        tag.save()    
        
        if p.tags.filter(name=tag_name).count() < 1:
            p.tags.add(tag)
            p.save()
        else:
            # poll already has that tag
            # silently fail
            pass

    vars["poll"] = p
    return render_to_response("ajax/list_poll_tags.html", vars)

def delete_poll_tag(request):
    """
    ajax handler to delete a poll tag
    from the poll creator 
    """
    tid = request.GET.get("tid", None)
    pid = request.GET.get("pid", None)    
    p = Poll.objects.get(id=pid)   #@UndefinedVariable
    # make sure user owns polls
    if p.user != request.user:
        return HttpResponseForbidden("unauthorized")
    
    pt = p.tags.get(id=tid)
    p.tags.remove(pt)
    p.save()

    pt.poll_count = pt.poll_count - 1
    pt.save()
    
    vars = {}
    vars["tags"] = p.tags.all()
    vars["poll"] = p

    return render_to_response("ajax/list_poll_tags.html", vars)


def poll_active(request, poll_id=None, choice=None):
    if poll_id == None or choice == None:
        return HttpResponse("not all vals")
    poll = Poll.objects.get(id=poll_id)   #@UndefinedVariable
    votes = PollVote.objects.filter(poll=poll).count()   #@UndefinedVariable
    if votes < consts.POLL_VOTES_BEFORE_PERMANENTLY_ACTIVE:
        active = '1' == choice
        poll.active = active
        poll.save()
        ret = "<span class='inactive-poll'>Inactive (Your poll is no longer available to other users.)</span>"
        if active: ret = "<span class='active-poll'>Active (Your poll is available to other users now.)</span>";
    else:
        ret = "<span class='active-poll'>Active (Your poll is permanently active.)</span>"
    return HttpResponse(content=ret)

def set_allow_user_answer(request, poll_id=None, choice=None):
    if poll_id == None or choice == None:
        return HttpResponse("not all vals")
    poll = Poll.objects.get(id=poll_id, active=False)   #@UndefinedVariable
    
    # make sure user owns polls
    if poll.user != request.user:
        return HttpResponseForbidden("unauthorized")
    
    choice = int(choice)
    if choice == 1:
        poll.allow_user_answers = True
        poll.save()
        return HttpResponse("will not")
    elif choice == 0:
        poll.allow_user_answers = False
        poll.save()
        return HttpResponse("will")
    
    return HttpResponse("bad")    

def show_video(request, poll_id):
    p = Poll.objects.get(id=poll_id)   #@UndefinedVariable
    if request.user != p.user:
        return HttpResponseForbidden("unauthorized")
    return HttpResponse(p.video_link)
    

##############################
# POLL VIEW / COMMENTS AJAX
###############################

def update_comment_count(request):
    pid = request.GET.get("pid", None)
    if pid == None:
        return HttpResponse("")
    poll = Poll.objects.get(id=pid)   #@UndefinedVariable
    # update count from model
    count = ThreadedComment.objects.filter(object_id=pid).count()
    poll.total_comments = count
    poll.save()
    return HttpResponse(str(count))

def update_comment(request):
    pid = request.GET.get("pid", None)
    if pid == None:
        return HttpResponse("")
    poll = Poll.objects.get(id=pid)   #@UndefinedVariable
    count = ThreadedComment.objects.filter(object_id=pid).count()
    poll.total_comments = count
    poll.save()
    return HttpResponse(str(count))

def delete_comment(request, object_id):
    pid = ThreadedComment.objects.get(id=object_id).object_id
    p = Poll.objects.get(id=pid)   #@UndefinedVariable
    p.total_comments = p.total_comments - 1
    p.save()
    return views.comment_delete(request, object_id=object_id)

def email_on_comment(request, object_id):
    log = logging.getLogger('pollajax.email_on_comment')
    comment = ThreadedComment.objects.get(id=object_id)
    poll = Poll.objects.get(id=comment.object_id)   #@UndefinedVariable
    if comment.parent_id:
        parent_comment = ThreadedComment.objects.get(id=comment.parent_id)
        user = parent_comment.user
        data = UserService(user=user).getUserData()
        if data.email_on_comment_reply:            
            # someone replied to your comment
            body = """Hello!<br/>It looks like %s has replied to your comment on the poll <a href="%s">%s</a>.  
            <br/>Just thought you'd like to know!
            <br/>
            Thanks!
            <br/>        
            P.S. If you'd like to turn off these emails you can visit your settings from the user profile page.
            """ % (comment.user, settings_local.HOST_NAME + "view-poll/" + poll.url + "/", poll.question)
            
            subject, from_email, to = '%s has replied to your comment' % comment.user, 'Pollstruck@gmail.com', parent_comment.user.email
            text_content = 'Hello!\nIt looks like %s has replied to your comment on the poll: %s.  Just thought you would like to know!\n\nThanks!\nP.S. If you would like to turn off these emails you can visit your settings from the user profile page.' % (comment.user, poll.question)
            html_content = body
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                # swallow zee exceptions!!
                log.error("could not send email to %s" % parent_comment.user.email)
            
    else:        
        data = UserService(user=poll.user).getUserData()
        # someone replied to your poll
        if data.email_on_poll_comment:
            body = """Hello!<br/>It looks like %s has commented on your poll <a href="%s">%s</a>.  
            <br/>Just thought you'd like to know!
            <br/>
            Thanks!
            <br/>        
            P.S. If you'd like to turn off these emails you can visit your settings from the user profile page.
            """ % (comment.user, settings_local.HOST_NAME + "view-poll/" + poll.url + "/", poll.question)
            
            subject, from_email, to = '%s has commented on your poll' % comment.user, 'Pollstruck@gmail.com', poll.user.email
            text_content = 'Hello!\nIt looks like %s has commented on your poll: %s.\nJust thought you would like to know!\n\nThanks!\nP.S. If you would like to turn off these emails you can visit your settings from the user profile page.' % (comment.user, poll.question)
            html_content = body
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                # KILL ZEE EXCEPTIONS
                log.error("could not send email to %s" % poll.user.email)
    return HttpResponse()

##############################
# POLL VIEW / DEMOGRAPHICS
###############################

user_profile_form = UserProfileDemoFilterForm()
choices = zip(user_profile_form.fields.keys(), user_profile_form.fields.keys())
choices.insert(0, (0, '---------------'))
class DemographicSelectForm(forms.Form):
    def __init__(self, count, *args, **kargs):
        super(DemographicSelectForm, self).__init__(*args, **kargs)
        self.fields['demographic_' + str(count)] = forms.ChoiceField(widget=forms.Select(attrs={'onchange':'return getDemographicValueForm();'}), choices=choices, required=True)

def demographic_form(request):
    counter = int(request.REQUEST['counter'])
    form = DemographicSelectForm(counter)
    return render_to_response("ajax/demographic_form.html", {'form':form, 'counter':counter})

age_is_choices = ((-1, 'is less than'), (0, 'is'), (1, 'is bigger than'))
def demographic_value_form(request):
    demographic = request.REQUEST['demographic']
    counter = int(request.REQUEST['counter'])
    
    class DynamicDemoValueForm(forms.Form):
        def __init__(self, demographic, count, *args, **kargs):
            super(DynamicDemoValueForm, self).__init__(*args, **kargs)
            value = copy.deepcopy(user_profile_form.fields[demographic])
            value.widget.attrs['onchange'] = 'return addedDemoValue();'

            if demographic == 'age' or demographic == 'income':
                self.fields['age_is_' + str(count)] = forms.ChoiceField(choices=age_is_choices, required=True)
            self.fields['demo_value_' + str(count)] = value


    form = DynamicDemoValueForm(demographic, counter)


    demo_value_name = 'demo_value_' + str(counter)
    vars = {'form_filter_value':form[demo_value_name], 'id':'id_' + demo_value_name, 'demographic':demographic}

    if 'age_is_' + str(counter) in form.fields:
        vars['form_age_is'] = form['age_is_' + str(counter)]

    vars['many2many'] = 0
    if form[demo_value_name].label == 'many2many':
        vars['many2many'] = 1

    vars['is_text_input'] = False
    if type(form.fields['demo_value_0']) is forms.CharField:
        vars['is_text_input'] = True

    return render_to_response("ajax/demographic_value_form.html", vars)
