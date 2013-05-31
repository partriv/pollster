'''
Created on Mar 8, 2009

@author: par
'''

class PollsterException(Exception):
    """
    Pollster exception
    """
    
    #log = LoggerFactory.getLoggerService().getLogger()
    
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)        

