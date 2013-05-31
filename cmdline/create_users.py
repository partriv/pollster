from django.contrib.auth.models import User
from pollster.models import Tag, UserProfile
import random
import sys

def create_users(num_users):
    for x in range(num_users):
        random_num = str(random.randint(0, sys.maxint))
        username = 'RandomUser' + random_num
        email = random_num + '@RandomUser.com'
        password = 'poopy'
        user = User.objects.create_user(username, email, password)


        tag_name = 'B' + str(random.randint(0, 15))
        try:
            tag = Tag.objects.get(name=tag_name)      #@UndefinedVariable
        except Tag.DoesNotExist:      #@UndefinedVariable
            tag = Tag(name=tag_name, poll_count=0)
            tag.save()
            
        user_profile = UserProfile(user=user)
        user_profile.save()
        user_profile.education.add(tag)
