'''
Created on May 12, 2009

@author: par
'''
import logging

import traceback


class middleware:
    """
    Exception handling middleware to intercept the 
    exception and output to a log file
    """
    
    log = logging.getLogger("ExceptionHandler")
    def process_exception(self, request, exception):
        self.log.fatal("Pollstruck fatal exception")
        self.log.fatal(traceback.format_exc())
        return None