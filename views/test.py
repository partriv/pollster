'''
Created on Mar 7, 2009

@author: par
'''
from pollster.views.base import base

from django.contrib.auth.decorators import login_required
from pollster.services.facebookservice import FacebookService
import logging


@login_required
def index(request):
    
    log = logging.getLogger('test')
    vars = {}
    #if not request.facebook.check_session(request):
    print 'test'
     
    """
    info = pyFacebook.users.getInfo([pyFacebook.uid], ['name', 'birthday',
    'affiliations', 'sex'])[0]
    print 'Your Name:     ', info['name']
    print 'Your Birthday: ', info['birthday']
    print 'Your Gender:   ', info['sex']

    """
        
    fb_service = FacebookService()
    fb = fb_service.getFacebookSession(request)
    friend_ids = fb.friends.get()
    info = fb.users.getInfo(friend_ids, ['name', 'pic'])
    vars["info"] = info
    uid = fb.users.getLoggedInUser()
    #uid = fb.uid
    log.debug("USER ID: " + str(uid))
    
    # YOU CAN DO THIS
    #fb.notifications.send(to_ids=[uid, friend_ids[0]], notification="Hey whats up!")    
    #fbml = '<fb:profile-action url="http://www.pollstruck.com/">Voted on some poll</fb:profile-action>'
    fbml = "par voted on this shit!!!!!"
    setit = fb.profile.setFBML(fbml, uid, fbml, '', '', fbml)
    
    log.debug("GET FBML: " + str(fb.profile.getFBML()))
    log.debug("FB SET: " + str(setit))
    
    #bundle = fb.feed.registerTemplateBundle(one_line_story_templates=["{*actor*} just voted on some poll on Pollstruck."] )
    #log.debug("REGISTER TEMPLATE BUNDLE: " + str(bundle))
    
    #fb.feed.publishUserAction(template_bundle_id=0, story_size=1)
    #fb.feed.publishStoryToUser(title="testing 123", body="This is a body")

    # CANT DO THESE
    #fb.users.setStatus(status='is updating his status from a secret place.', clear=False, uid=uid)
    #fb.feed.publishActionOfUser(title="testing 123", body="This is a body")
    #fb.feed.publishStoryToUser(title="Testing 123", body="testing body")        
    #fb.stream.publish(message='Testing 123')


    return base.render(request=request, template="test.html", vars=vars)

    