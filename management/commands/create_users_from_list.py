'''
Created on Jun 1, 2009

@author: par
'''
from pollster.services.userservice import UserService
from django.core.management.base import NoArgsCommand
from pollster.exception.pexception import PollsterException
import logging

class Command(NoArgsCommand):
    help = "makes some users from a list"

    requires_model_validation = False

    log = logging.getLogger('make users from a list')

    def handle_noargs(self, **options):
        users = ["yoyo_champion", "speakerbox", "camera-obscura", "chessmstr9000", "beerguy25", "LA girl", "bikethief", 
                 "punkyparty", "jonjon", "nkomar", "tracerbullet", "napolean", "polldancer", "answer_master", 
                 "slashdot_guy", "power_poller", "stlcl", "smither palmer", "23skidoo", "leslie anne", "mary w", "charleswes",
                 "jerkateer", "band-aid", "cameragirl", "brodeo5000", "mona lisa", "cigbum", "toker", "superdrunkie", "moleskinnotebook",
                 "needanotherbeer", "superbutt", "shopping maniac", "disco stu", "chef", "sgt terry", "wolfshirt",
                 "ted streetcar", "dc", "ew", "dakur", "starpony", "zoop", "higgins", "nineve", "salstress", "mario",
                 "miaux", "theo", "millicent", "moss", "multimind", "sefafim", "dddave", "bukowski", "misses", "xartet",
                 "bougyman", "merreck", "magus", "igor", "furcifer"]
        
        print len(users)
        raise PollsterException("Are you sure you are creating new users?")
        for user in users:
            user = UserService().createUser(username=user, email=user + "@parsworld.com", password="foo")
            self.log.debug('created %s' % user.username)