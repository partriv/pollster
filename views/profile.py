'''
Created on Mar 8, 2009

@author: par
'''
from pollster.views.base import base
from pollster.models import Poll, UserProfile, Tag, ScreenName, PollVote,\
    PollsterMessage
from pollster.consts import consts

from django.contrib import auth
from django.http import HttpResponseRedirect, HttpResponse,\
    HttpResponseForbidden, HttpResponseServerError, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USStateField, USZipCodeField
from pollster.services.poll import PollService
from django.forms.fields import CharField, FileField
from django.forms.widgets import Textarea, PasswordInput
from django.core.paginator import Paginator
from pollster.services.userservice import UserService
from pollster.utils import paging_utils, string
from django.core.mail import send_mail
from random import choice
from threadedcomments.models import ThreadedComment
import datetime
import logging

@login_required
def commented(request, username, page_num=1):
    user = User.objects.get(username=username)    
    comments = ThreadedComment.objects.filter(user=user)
    poll_ids = [c.object_id for c in comments]
    polls = Poll.objects.filter(active=True, id__in=poll_ids).order_by('-date_modified')   #@UndefinedVariable
    return index(request, username, polls, {"class":"commented-view"}, page_num=page_num, page_link_prefix="/profile/%s/commented" % username)

@login_required
def not_finished(request, username=None, page_num=1):
    user = User.objects.get(username=username)
    if username != request.user.username:
        return HttpResponseRedirect("/profile/%s/" % request.user.username)
    else:        
        polls = Poll.objects.filter(user=user, active=False).order_by('-date_modified')   #@UndefinedVariable
    return index(request, username, polls, {"class":"not-finished-view"}, page_num=page_num, page_link_prefix="/profile/%s/not-finished" % username)

@login_required
def created(request, username=None, page_num=1):
    user = User.objects.get(username=username)
    if username == request.user.username:
        polls = Poll.objects.filter(user=user).order_by('-date_created')   #@UndefinedVariable
    else:        
        polls = Poll.objects.filter(user=user, active=True).order_by('-date_created')   #@UndefinedVariable
    return index(request, username, polls, {"class":"created-view"}, page_num=page_num, page_link_prefix="/profile/%s/created" % username)
    
@login_required
def voted_on(request, username=None, page_num=1):
    log = logging.getLogger('profile')
    # TODO: ssecurity/settings check
    user = User.objects.get(username=username)
    votes = PollVote.objects.filter(user=user).order_by('-date_created')   #@UndefinedVariable
    polls = []
    for v in votes:
        polls.append(v.poll)    
    return index(request, username, polls, {"class":"voted-on-view"}, page_num=page_num, page_link_prefix="/profile/%s/voted-on" % username)

@login_required
def watching(request, username=None, page_num=1):
    us = UserService(user=User.objects.get(username=username))
    polls = us.getPollsWatched()
    return index(request, username, polls, {"class":"watch-view"}, page_num=page_num, page_link_prefix="/profile/%s/watching" % username)


@login_required
def index(request, username=None, polls=None, vars=None, page_num=1, page_link_prefix=None):
    #if vars == None:
    #    return voted_on(request, username=username, page_num=page_num)
        #vars = {"class":"index-view"}
        
    user_for_profile = None
    if username == None:
        # if no username specified then just display 
        # profile of user who is logged in
        user_for_profile = request.user
    else:
        user_for_profile = User.objects.get(username=username)    
    vars["user_for_profile"] = user_for_profile
    
    vars['show_ad'] = True

    # get some sweet user stats!
    total_polls_count = Poll.objects.filter(active=1).count() #@UndefinedVariable
    user_polls_count = Poll.objects.filter(user=user_for_profile, active=1).count() #@UndefinedVariable
    vars["user_polls_count"] = user_polls_count
    if total_polls_count > 0:
        vars["user_polls_percent"] = (1.0 * user_polls_count / total_polls_count) * 100
    user_comments_count = 0
    poll_set = set()
    for tc in ThreadedComment.objects.filter(user=user_for_profile):
        poll_set.add(tc.object_id)
        user_comments_count+=1
    vars["user_comments_count"] = user_comments_count
    vars["user_poll_comments"] = len(poll_set)
    user_votes_count = PollVote.objects.filter(user=user_for_profile).count() #@UndefinedVariable
    vars["user_votes_count"] = user_votes_count
    if total_polls_count > 0:
        vars["user_votes_percent"] = (1.0 * user_votes_count / total_polls_count) * 100
        
    
    # check owner
    owner = user_for_profile.username == request.user.username
    vars["owner"] = owner

    # pass in the logged in user
    if not vars.has_key('activity'):
        if not page_link_prefix:
            page_link_prefix = "/profile/%s" % user_for_profile.username        
        polls = PollService().getPollsForLister(polls, request.user, page_num=page_num, page_link_prefix=page_link_prefix)
        vars.update(polls)
    else:
        pass
        
    vars["user_prof_data"] = UserService(user_for_profile).getUserData()
    vars["messageForm"] = MessageForm()
    return base.render(request, "user/profile.html", vars)

@login_required
def activity_home_index(request, username=None):
    vars = {}
    user = User.objects.get(username=username)
    owner = request.user == user
    activity, remain = PollService().getUserFeed(user=user, owner=owner, request_user=request.user)
    vars["activity"] = activity
    vars["remain"] = remain
    vars['class'] = 'activity-feed'
    return index(request, username, polls=None, vars=vars, page_num=1, page_link_prefix='/profile/%s/activity/')
    
@login_required
def activity_index(request, username=None):
    vars = {}
    phase = int(request.GET.get('phase', 0))    
    user_for_profile = User.objects.get(username=username)
    owner = user_for_profile == request.user
    vars["owner"] = owner
    activity, remain = PollService().getUserFeed(user=user_for_profile, owner=owner, phase=phase, request_user=request.user)
    vars["activity"] = activity
    vars["remain"] = remain
    vars["user_for_profile"] = user_for_profile
    vars["datetimenow"] = datetime.datetime.now()
    if remain:
        return base.render(request=request, template="user/profile-activity-lister.html", vars=vars)
    else:
        return HttpResponse(content="0")

    
    

##############################
##                          ##
# #                        # #
#  ########################  #
#                            #
#         MAIL BOX           #
#                            #
##############################
@login_required
def mail(request, username=None):
    """
    handles ajax send of message
    """
    log = logging.getLogger('mail')
    
    subject = request.POST.get("subject", None)
    body = request.POST.get("body", None)
    mid = request.POST.get("mid", None)
    if mid == 'undefined':
        mid = None

    # get user who message is to
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:  #@UndefinedVariable
        log.warning("Attempt to send mail to invalid user: %s done by user: %s" % (username, request.user.username))        
        return HttpResponse(content="<img src=\"/i/icons/email_delete.png\"/> Your message was not sent - 101") 
    
    if not body or body.strip() == "":
        return HttpResponse(content="<img src=\"/i/icons/email_delete.png\"/> You need to provide a message")
    
    if user == request.user:
        return HttpResponseForbidden("D'oh! ;)")    

    body = string.strip(body)
    body = body.replace("\n", "<br/>")
    if mid:        
        old_msg = PollsterMessage.objects.get(id=mid)   #@UndefinedVariable
        old_body = old_msg.body
        old_arr = old_body.split("<br/>")
        old_body = ""
        for msg_chnk in old_arr:
            old_body += "> " + msg_chnk + "<br/>"
        body = str(body) + "<br/><br/>Previous message from " + str(old_msg.from_user.username) + "<hr/><br/>" + str(old_body)
    
    # create message
    ps = PollService()
    ps.sendPollsterMessage(to_user=user, from_user=request.user, subject=subject, body=body)
    
    return HttpResponse(content="<img src=\"/i/icons/email_go.png\"/> Your message has been sent!")

@login_required
def mark_mail_read(request):
    msgs = PollsterMessage.objects.filter(to_user=request.user)   #@UndefinedVariable
    for msg in msgs:
        msg.read = True
        msg.save()    

@login_required
def mail_view(request, username=None, page_num=1): 
    """
    mail view controller
    """
    id = request.GET.get("id", None)
    if id:
        # request to mark mail as read
        msg = PollsterMessage.objects.get(id=id)     #@UndefinedVariable
        if msg.to_user == request.user:
            # make sure the person who owns the message is marking it
            msg.read = True
            msg.save()
        else:
            return HttpResponseForbidden("Nope! :)")
        return HttpResponse(content="happy success!")
    
    # YOU CAN ONLY DO IT FOR URESELF
    if username != request.user.username:
        return HttpResponseRedirect("/profile/%s/mail/view/" % request.user.username)
    
    vars = {}
    
    messages = PollsterMessage.objects.filter(to_user=request.user)   #@UndefinedVariable
    vars["msgCount"] = messages.count()    
    paginator = Paginator(messages.order_by('-date_created'), 20)
    vars["paginator"] = paginator
    vars["page"] = paginator.page(page_num)

    page_hash = paging_utils.setup_page_hash(paginator=paginator, page_num=page_num, page_link_prefix="/profile/%s/mail/view" % username)
    vars.update(page_hash)
    
    vars["messageForm"] = MessageForm()
    return base.render(request, "user/mailview.html", vars)

@login_required
def mail_sent(request, username=None, page_num=1): 
    """
    mail view controller
    """
    # YOU CAN ONLY DO IT FOR URESELF
    if username != request.user.username:
        return HttpResponseRedirect("/profile/%s/mail/view/" % request.user.username)
    
    vars = {}
    messages = PollsterMessage.objects.filter(from_user=request.user)   #@UndefinedVariable
    vars["msgCount"] = messages.count()    
    paginator = Paginator(messages.order_by('-date_created'), 20)
    vars["paginator"] = paginator
    vars["page"] = paginator.page(page_num)

    page_hash = paging_utils.setup_page_hash(paginator=paginator, page_num=page_num, page_link_prefix="/profile/%s/mail/sent" % username)
    vars.update(page_hash)
    
    vars["messageForm"] = MessageForm()
    vars["sent_mode"] = True    
    return base.render(request, "user/mailview.html", vars)
    

class MessageForm(forms.Form):
    subject = CharField(max_length=100)
    body = CharField(max_length=1500, widget=Textarea())

########################
#
# FORGOT MY SUTFF!
#
#########################
def forgot_username(request):
    
    email = request.GET.get("email", None)
    user = User.objects.get(email=email)
    msg = "Hello from Pollstruck.  We've got your username right here!\nYour username is %s.\n\nSee ya soon!\n-Pollstruck" % user.username
    send_mail('Your username', msg, 'Pollstruck@gmail.com', [email], fail_silently=False)
    return HttpResponse(content="Username sent!")

def forgot_password(request):
    email = request.GET.get("email", None)
    user = User.objects.get(email=email)
    newpw = ''.join([choice('QWERTYUOPASDFGHJKLZXCVBNM') for i in range(7)])
    user.set_password(newpw)
    user.save()
    send_mail('Your new password', 'Your new password is: %s.  Your password is case sensitive!' % newpw, 'Pollstruck@gmail.com', [email], fail_silently=False)
    return HttpResponse(content="Your new password is: %s.  Write this down and keep it safe.  You can also change it from your profile page.  This password has been emailed to you as well." % newpw)


class ChangePasswordForm(forms.Form):
    old_password = CharField(widget=PasswordInput())
    new_password = CharField(widget=PasswordInput())
    confirm_new_password = CharField(widget=PasswordInput())

def change_password(request, username=None):
    user = User.objects.get(username=username)
    if request.user != user:
        return HttpResponseNotFound()
    vars = {}
    
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_pw = form.cleaned_data["old_password"]
            new_pw = form.cleaned_data["new_password"]
            conf_new_pw = form.cleaned_data["confirm_new_password"]
            if user.check_password(old_pw):
                if new_pw == conf_new_pw:
                    user.set_password(new_pw)
                    user.save()
                    return HttpResponseRedirect("/profile/%s/" % user.username)
                else:
                    vars["error"] = "Your passwords do not match"    
            else:
                vars["error"] = "Your old password is incorrect"
        vars["form"] = form                            
    else:
        vars["form"] = ChangePasswordForm()
    return base.render(request=request, template="user/change_password.html", vars=vars)
    

########################
#
# LETS BE FRIENDS
#
#########################

@login_required
def friend(request):
    id = request.GET.get("id")
    user = User.objects.get(id=id)
    if request.user == user:
        return HttpResponseForbidden("Nope!!")
    
    us = UserService(request.user)
    data = us.getUserData()
    # add friend
    data.friends.add(user)
    data.save()
    
    # do reverse as well
    # TODO: check user settings before auto adding this
    
    to_data = UserService(user).getUserData()
    # add friend
    to_data .friends.add(request.user)
    to_data.save()
    
    # notify user
    ps = PollService()
    subject = "%s added you as  friend" % request.user.username
    body = "Hi, %s has just added you as a friend.  As a result %s has been automatically added to your friends list.\n This is because he/she added you to their list.  You can change this setting in your settings if you like." % (request.user.username, request.user.username)
    ps.sendPollsterMessage(to_user=user, from_user=request.user, subject=subject, body=body)    
    
    return HttpResponse(content="You are now friends!")

@login_required
def logout(request):
    auth.logout(request)
    if request.session.has_key('session_key'):
        del request.session['session_key']
    if request.session.has_key('uid'):
        del request.session['uid']
    return HttpResponseRedirect("/")


def convert_to_choices(dict):
    choices = []
    for key, value in dict.items():
        choices.append((key, value))
    return choices

########################
#
# USER PICTURE
#
#########################
class ProfilePicForm(forms.Form):
    file = FileField(required=False)

@login_required
def pic(request, username=None):
    vars= {}
    user = User.objects.get(username=username)
    if user != request.user:
        return HttpResponseForbidden("NopeLOL!")
    us = UserService(user)
    data = us.getUserData()
    if data.profile_pic:
        vars["pic"] = data.profile_pic
    
    form = ProfilePicForm()
    if request.method == 'POST':
        form = ProfilePicForm(request.POST)
        if form.is_valid():
            f = request.FILES['file']
            us.uploadUserPic(f)
            return HttpResponseRedirect("/profile/%s/pic/" % username)
        
    vars["form"] = form
    
    return base.render(request=request, template="user/profile_pic.html", vars=vars)


############################################################################
#
#
#  USER PROFILE STUFF
#
#
############################################################################


income_choices = convert_to_choices(consts.PROFILE_INCOME_ENGLISH)
sex_choices = convert_to_choices(consts.PROFILE_SEX_ENGLISH)
country_choices = convert_to_choices(consts.PROFILE_COUNTRY_CODES)
ethnicity_choices = convert_to_choices(consts.PROFILE_ETHNICITY)
interested_in_choices = convert_to_choices(consts.PROFILE_SEXES_ENGLISH)
relationship_status_choices = convert_to_choices(consts.PROFILE_RELATIONSHIP_STATUS)
screen_name_service_choices = convert_to_choices(consts.PROFILE_IM_SERVICES)


class UserProfileBaseForm(forms.Form):
    sex = forms.ChoiceField(choices=sex_choices, required=False)
    country = forms.ChoiceField(choices=country_choices, required=False)
    city = forms.CharField(max_length=64, required=False)
    state = USStateField(required=False)
    zip_code = USZipCodeField(required=False)
    income = forms.ChoiceField(choices=income_choices, required=False)
    ethnicity = forms.ChoiceField(choices=ethnicity_choices, required=False)
    sexual_orientation = forms.ChoiceField(choices=interested_in_choices, required=False)
    relationship_status = forms.ChoiceField(choices=relationship_status_choices, required=False)
    political = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}),max_length=30, required=False)
    religious = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}),max_length=30, required=False)
    education = forms.CharField(widget=forms.TextInput(attrs={'autocomplete':'off'}), max_length=64, required=False)
    work = forms.CharField(widget=forms.TextInput(attrs={ 'autocomplete':'off'}), max_length=64, required=False)

age_choices = zip(range(1,100), range(1,100))
class UserProfileDemoFilterForm(UserProfileBaseForm):
    age = forms.ChoiceField(choices=age_choices, required=False)

    # we use the label just to store an attribute, not a wonderful solution :'(
    interests = forms.CharField(label="many2many", widget=forms.TextInput(attrs={'autocomplete':'off'}), required=False)
    music = forms.CharField(label="many2many", widget=forms.TextInput(attrs={'autocomplete':'off'}), required=False)
    tv = forms.CharField(label="many2many", widget=forms.TextInput(attrs={'autocomplete':'off'}), required=False)
    books = forms.CharField(label="many2many", widget=forms.TextInput(attrs={'autocomplete':'off'}), required=False)
    movies = forms.CharField(label="many2many", widget=forms.TextInput(attrs={'autocomplete':'off'}), required=False)

class UserProfileForm(UserProfileBaseForm):
    birthday = forms.DateField(required=False)
    phone = USPhoneNumberField(required=False)
    about = forms.CharField(widget=forms.Textarea(), required=False)
    screen_name = forms.CharField(max_length=40, required=False)
    screen_name_service = forms.ChoiceField(choices=screen_name_service_choices, required=False)

    interests = forms.CharField(widget=forms.Textarea(), required=False)
    music = forms.CharField(widget=forms.Textarea(), required=False)
    tv = forms.CharField(widget=forms.Textarea(), required=False)
    books = forms.CharField(widget=forms.Textarea(), required=False)
    movies = forms.CharField(widget=forms.Textarea(), required=False)


@login_required
def edit(request, username=None):
    if username != request.user.username:
        return HttpResponseRedirect("/")
    
    user = request.user

    try:
        user.get_profile()
    except auth.models.SiteProfileNotAvailable:
        pass

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            try:
                user_profile = UserProfile.objects.get(user=user)   #@UndefinedVariable
            except UserProfile.DoesNotExist:   #@UndefinedVariable
                user_profile = UserProfile(user=user)
                user_profile.save()
            
            user_profile.sex = int(form.cleaned_data['sex'])
            user_profile.income = form.cleaned_data['income']
            user_profile.ethnicity = form.cleaned_data['ethnicity']
            user_profile.sexual_orientation = form.cleaned_data['sexual_orientation']
            user_profile.relationship_status = form.cleaned_data['relationship_status']
            user_profile.country = form.cleaned_data['country']
            user_profile.birthday = form.cleaned_data['birthday']
            user_profile.city = form.cleaned_data['city'] 
            user_profile.state = form.cleaned_data['state']
            user_profile.zip_code = form.cleaned_data['zip_code']
            user_profile.phone = form.cleaned_data['phone']
            user_profile.about = form.cleaned_data['about']

            def save_tag(form_field):
                if str(form_field):
                    try:
                        tag = Tag.objects.get(name=form_field)   #@UndefinedVariable
                    except Tag.DoesNotExist:   #@UndefinedVariable
                        tag = Tag(name=form_field, poll_count=0)
                        tag.save()
                    return tag
                return None
                

            tag = save_tag(form.cleaned_data['education'])
            user_profile.education = tag

            tag = save_tag(form.cleaned_data['work'])
            user_profile.work = tag

            tag = save_tag(form.cleaned_data['political'])
            user_profile.political = tag

            tag = save_tag(form.cleaned_data['religious'])
            user_profile.religious = tag


            def save_comma_tags(user_profile, form_field,  form_field_name):
                tags = form_field.split(',')
                for tag in tags:
                    tag = tag.strip(' ')
                    tag = save_tag(tag)
                    if tag:
                        getattr(user_profile, form_field_name).add(tag)
                
            save_comma_tags(user_profile, form.cleaned_data['interests'], 'interests')
            save_comma_tags(user_profile, form.cleaned_data['music'], 'music')
            save_comma_tags(user_profile, form.cleaned_data['tv'], 'tv')
            save_comma_tags(user_profile, form.cleaned_data['books'], 'books')
            save_comma_tags(user_profile, form.cleaned_data['movies'], 'movies')


#            user_profile.screen_name = form.cleaned_data['screen_name'] + '||' + form.cleaned_data['screen_name_service']

            user_profile.save()
            ScreenName(screen_name=form.cleaned_data['screen_name'], service=form.cleaned_data['screen_name_service'], user_profile=user_profile).save()

    else:
        try:
            user_profile = UserProfile.objects.get(user=user)   #@UndefinedVariable
            education = ''
            if user_profile.education:
                education = user_profile.education.name

            work = ''
            if user_profile.work:
                work = user_profile.work.name

            political = ''
            if user_profile.political is not None:
                political = user_profile.political.name

            religious = ''
            if user_profile.religious is not None:
                religious = user_profile.religious.name

            def get_all_tags(tag_name):
                tags = ''
                if getattr(user_profile, tag_name) is not None:
                    query_set = getattr(user_profile, tag_name).all()
                    all_tags = []
                    for q in query_set:
                        all_tags.append(q.name)
                    tags = ', '.join(all_tags)
                return tags
                

            interests = get_all_tags('interests')
            music = get_all_tags('music')
            tv = get_all_tags('tv')
            books = get_all_tags('books')
            movies = get_all_tags('movies')

            initial = {'sex':user_profile.sex, 'birthday':user_profile.birthday, 'country':user_profile.country,
                       'city':user_profile.city, 'state':user_profile.state, 'zip_code':user_profile.zip_code, 'phone':user_profile.phone,
                       'income':user_profile.income, 'ethnicity':user_profile.ethnicity, 'sexual_orientation':user_profile.sexual_orientation,
                       'relationship_status':user_profile.relationship_status, 'political':political, 'religious':religious,
                       'about':user_profile.about, 'education':education, 'work':work, 'interests':interests, 'music':music, 'tv':tv,
                       'books':books, 'movies':movies}
            form = UserProfileForm(initial=initial)
        except UserProfile.DoesNotExist:   #@UndefinedVariable
            form = UserProfileForm(initial={'country':consts.PROFILE_UNITED_STATES})
        

    vars = {}

    vars['form'] = form
    return base.render(request, "user/profile_edit.html", vars)

