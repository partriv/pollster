'''
Created on May 19, 2009

@author: par
'''
#from facebook.djangofb import Facebook
import logging
import md5
import pollster.settings

class FacebookService():
    
    log = logging.getLogger('Facebook Service')
    
    def getFacebookSession(self, request):
        fb = Facebook(settings.FACEBOOK_API_KEY, settings.FACEBOOK_SECRET_KEY)
        if 'session_key' in request.session and 'uid' in request.session:
            fb.session_key = request.session['session_key']
            fb.uid = request.session['uid']
        else:
            self.log.debug("Could not get fb session from user session, trying cookies")
            if settings.FACEBOOK_API_KEY + '_session_key' in request.COOKIES and settings.FACEBOOK_API_KEY + '_uid' in request.COOKIES:                
                request.session['session_key'] = request.COOKIES[settings.FACEBOOK_API_KEY + '_session_key'] 
                request.session['uid'] = request.COOKIES[settings.FACEBOOK_API_KEY + '_uid']
                fb.session_key = request.session['session_key']
                fb.uid = request.session['uid']
                self.log.debug("Success from cookies")
            else:
                self.log.debug("Could not initialize facebook service!")
                return None
        return fb

    def getUserPassword(self, fb_id):
        # create the facebook user password based on a has of my django apps secret key and their fb user id
        m = md5.new()
        m.update(settings.SECRET_KEY + str(fb_id))
        return m.hexdigest()
