from pollster.models import Poll, PollAnswer, PollVote
from django.contrib.auth.models import User
import random
import sys

def add_random_answers(poll_id, num_answers, create_new=False, user=None):
    poll = Poll.objects.get(pk=poll_id)      #@UndefinedVariable
    poll_answers = list(PollAnswer.objects.filter(poll=poll))      #@UndefinedVariable
    users = User.objects.filter(username__contains='RandomUser')
    letters = list("abcdefghijklmnopqrstuvwxyz")
    if users.count() < num_answers:
        sys.exit("There are %d users, not enough for %d answers" % (users.count(), num_answers))

    answers = 0
    user_index = 0
    while answers < num_answers:
        try:
            user_voted = PollVote.objects.filter(poll=poll, user=users[user_index]).count() > 0      #@UndefinedVariable
            if not user_voted:
                if create_new == False:
                    rand_poll_answer = poll_answers[random.randint(0, len(poll_answers) - 1)]
                else:
                    # generate a new answer for each user voting
                    new_ans = PollAnswer()
                    new_ans.poll = poll
                    random_word = ""
                    for i in range(0,5):
                        random_word += letters[random.randint(0, len(letters)-1)]
                    new_ans.answer = random_word
                    new_ans.user=users[user_index]
                    new_ans.save()
                    rand_poll_answer = new_ans 
                poll_vote = PollVote(poll=poll, poll_answer=rand_poll_answer, user=users[user_index])
                poll_vote.save()
                answers += 1
                poll.total_votes += 1
                poll.save()                
        except IndexError:
            sys.exit("Only made %d answers, not enough users who havent voted" % answers)
        user_index += 1
        
