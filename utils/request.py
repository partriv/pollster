'''
Created on Apr 3, 2009

@author: par
'''

class RequestUtils():
    
    @staticmethod
    def getCurrentUser(request):
        if request.user.is_authenticated():
            return request.user
        return None