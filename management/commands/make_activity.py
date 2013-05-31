'''
Created on Jun 1, 2009

@author: par
'''
from django.contrib.auth.models import User
from pollster.services.poll import PollService
from pollster.models import PollAnswer, PollVote
from django.core.management.base import BaseCommand, NoArgsCommand
from pollster.conf.settings_local import USER_IDS_TO_CREATE
from pollster.views import pollview
import logging
import random




class Command(NoArgsCommand):
    help = "Runs the make activity shindig"

    requires_model_validation = False

    def handle_noargs(self, **options):
        self.random_vote_by_user()
    
    def random_vote_by_user(self):
        valid_user_index = random.randint(0, len(USER_IDS_TO_CREATE)-1)
        user_id = USER_IDS_TO_CREATE[valid_user_index]
        user = User.objects.get(id=user_id)
        ps = PollService()
        user_new_polls = ps.get_polls_user_has_not_voted_on(user=user, return_all=False)
        if user_new_polls:
            index = random.randint(0, len(user_new_polls)-1)
            poll = user_new_polls[index]
            print "Selecting from %d polls" % len(user_new_polls)
            poll_answers = list(PollAnswer.objects.filter(poll=poll))      #@UndefinedVariable
            rand_poll_answer = poll_answers[random.randint(0, len(poll_answers) - 1)]
            
            poll_vote = PollVote(poll=poll, poll_answer=rand_poll_answer, user=user)        
            poll_vote.save()
            
            poll.total_votes += 1
            poll.save()   
            pollview.send_voted_email(to_email=poll.user.email, from_user=user, poll=poll)
            
            print "User: '%s'\nVoted on poll: '%s'\nAnswer: '%s'" % (user.username, poll.question, rand_poll_answer.answer) 
        else:
            print "Could not vote, user has voted on all polls: %s" % user.username            
        return False