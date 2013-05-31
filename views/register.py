from pollster.views.base import base
from pollster.consts import consts
from django import forms
from django.contrib.auth import models
from django.forms.fields import CharField, EmailField, BooleanField
from django.forms.widgets import PasswordInput, HiddenInput, TextInput
from django.http import HttpResponseRedirect, HttpResponseNotFound,\
    HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
# random generator
from random import choice
# PIL elements, sha for hash
from PIL import Image, ImageDraw, ImageFont
from pollster.conf import settings_local
from pollster.utils.string import StringUtils
from pollster.services.userservice import UserService
from facebook.djangofb import Facebook
from pollster.services.facebookservice import FacebookService
import pollster.settings as settings
import sha

SALT = settings.SECRET_KEY[:20]

class RegForm(forms.Form):
    name = CharField(max_length=30, required=False)
    username = CharField(min_length=2, max_length=30, 
                         help_text="30 characters or fewer. Alphanumeric characters only (letters, digits and underscores)", 
                         widget=TextInput(attrs={"onfocus":"showRegHelp('username');", "onblur":"hideRegHelp('username');return checkUsername();"}))
    email = EmailField()
    password = CharField(widget=PasswordInput)
    confirm_password = CharField(widget=PasswordInput)
    next = CharField(widget=HiddenInput(), required=False)
    imghash = CharField(widget=HiddenInput(), required=True)
    imgtext = CharField(required=True, 
                        help_text="Please be case sensitive.  'A' is not the same as 'a'.", 
                        widget=TextInput(attrs={"onfocus":"showRegHelp('captcha');", "onblur":"hideRegHelp('captcha')"}))
    agree_to_terms = BooleanField(required=True)
    
    
def cleanName(name):
    return StringUtils.cleanWordForUrl(name)

def checkname(request):
    """
    ajax handler to check name during
    registration process
    """
    name = request.GET.get("n", "").strip()    
    if len(name) < 2:
        return HttpResponse(content="")
    name = cleanName(name)    
    if models.User.objects.filter(username=name).count() > 0:
        return HttpResponse(content="<img src='/i/icons/delete.png'/> Sorry, that username is not available.")
    else:
        return HttpResponse(content="<img src='/i/icons/accept.png'/> That username is available.")

def index(request):
    next = request.GET.get("next", None)
    if request.user.is_authenticated():
        if next:
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect('/')
    vars = {}
    if request.method == 'POST': # If the form has been submitted...
        cap_image = request.META['REMOTE_ADDR'] + '.jpg'
        
        form = RegForm(request.POST) # A form bound to the POST data        
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data["name"]
            if name and name != "":
                #  check the name honey pot,
                # if it has anything, return a 404, as to confuse
                # the ... SCUM BAGS!
                return HttpResponseNotFound(content="Not found")
            
            if form.cleaned_data["username"].strip() == "":
                return base.render(request, "register.html", {"cap_image":cap_image, "form":form, "error":"Please enter a valid username"})
            if form.cleaned_data["password"] != form.cleaned_data["confirm_password"]:
                return base.render(request, "register.html", {"cap_image":cap_image, "form":form, "error":"Passwords do not match"})
            if models.User.objects.filter(username=form.cleaned_data["username"]).count() > 0:
                return base.render(request, "register.html", {"cap_image":cap_image, "form":form, "error":"User exists"})
            if models.User.objects.filter(email=form.cleaned_data["email"]).count() > 0:
                return base.render(request, "register.html", {"cap_image":cap_image, "form":form, "error":"Email exists"})
            if form.cleaned_data['imghash'] != sha.new(SALT+form.cleaned_data['imgtext']).hexdigest():         
                return base.render(request, "register.html", {"cap_image":cap_image, "form":form, "error":"Please enter the correct text"})
             
            # register the user
            username = cleanName(form.cleaned_data["username"])
            user = UserService().createUser(username=username, email=form.cleaned_data["email"], password=form.cleaned_data["password"])
            if user is not None:
                auth.login(request, user)
            
            # check redirects
            next = form.cleaned_data.get("next", None)
            if next.strip() ==  "": next = None
            
            if next:
                return HttpResponseRedirect(next) # Redirect after POST
            return HttpResponseRedirect('/register/thanks/') # Redirect after POST
    else:
        imghash, imgname = get_captcha(request)
        cap_image = imgname
        initial = {"next":next, "imghash":imghash}
        form = RegForm(initial=initial) # An unbound form
        
    vars["cap_image"] = cap_image
    vars["form"] = form
    return base.render(request, "register.html", vars)

@login_required
def thanks(request):
    return base.render(request, "thanks_register.html")
        

def get_captcha(request):
        # create a 5 char random strin and sha hash it, note that there is no big i
        cstr = 'qwertyuiopasdfghjklzxcvbnmQWERTYUOPASDFGHJKLZXCVBNM'
        imgtext = ''.join([choice(cstr) for i in range(7)])
        # create hash
        imghash = sha.new(SALT+imgtext).hexdigest()
        
        # create an image with the string
        # PIL - open image, add text using font, save as new
        im=Image.open(settings_local.IMAGES_ROOT + "cap_bg.jpg")
        draw=ImageDraw.Draw(im)
        # font_file = 'MISTRAL.TTF'
        font_file = 'MTCORSVA.TTF'
        font=ImageFont.truetype(settings_local.FONTS_DIR + font_file, 38)
        draw.text((25,0),imgtext, font=font, fill=(20,60,60))
        #draw.line((10, 15, im.size[0]-15, im.size[1]-15), fill=(20,60,60))
        draw.line((2, 6, im.size[0], 50), fill=(20,60,60))
        #draw.line((0, im.size[1], im.size[0], 0), fill=128)

        # save as a temporary image
        # use user IP for the filename
        temp = settings_local.CAPTCHA_IMAGES_ROOT + request.META['REMOTE_ADDR'] + '.jpg'
        tempname = request.META['REMOTE_ADDR'] + '.jpg'
        im.save(temp, "JPEG")
        return (imghash, tempname)




