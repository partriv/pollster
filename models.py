from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    poll_count = models.IntegerField()

class Poll(models.Model):
    question = models.CharField(max_length=75)
    description = models.CharField(max_length=400)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    active = models.BooleanField(default=False)    
    user = models.ForeignKey(User)
    url = models.CharField(max_length=75)
    link = models.CharField(max_length=250)
    total_votes = models.IntegerField()
    total_comments = models.IntegerField()
    allow_user_answers = models.BooleanField(default=True)
    video_link = models.CharField(max_length=800)
    tags = models.ManyToManyField(Tag, null=True,related_name='poll_set_tags')
    inappropriate = models.BooleanField(default=False)

class PollFile(models.Model):
    poll = models.ForeignKey(Poll)
    file = models.CharField(max_length=100)
    main_file = models.CharField(max_length=100, default=False)

class PollAnswer(models.Model):
    poll = models.ForeignKey(Poll)
    answer = models.CharField(max_length=70)
    user = models.ForeignKey(User)

class PollVote(models.Model):
    poll = models.ForeignKey(Poll)
    date_created = models.DateTimeField(auto_now_add=True)
    poll_answer = models.ForeignKey(PollAnswer)
    user = models.ForeignKey(User)

class PollsterMessage(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    to_user = models.ForeignKey(User, related_name='pollstermessage_set_to_user')
    from_user = models.ForeignKey(User, related_name='pollstermessage_set_from_user')
    subject = models.CharField(max_length=100, null=True)
    body = models.CharField(max_length=1500)
    read = models.BooleanField(default=False)

class PollWatch(models.Model):
    poll = models.ForeignKey(Poll)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

class UserData(models.Model):
    user = models.ForeignKey(User, unique=True)
    polls_watched = models.ManyToManyField(PollWatch, null=True, related_name='userdata_set_polls_watched')
    friends = models.ManyToManyField(User, null=True, related_name='userdata_set_friends')
    profile_pic = models.CharField(max_length=255, default="happy_guy.jpg")
    link_in_new_window = models.BooleanField(default=True)
    default_chart_type = models.CharField(max_length=60, default='pie')
    facebook_id = models.IntegerField(null=True)
    use_profile_pic = models.BooleanField(default=True)
    email_on_vote = models.BooleanField(default=True)
    email_on_poll_comment = models.BooleanField(default=True)
    email_on_comment_reply = models.BooleanField(default=True)
    
import re
from django.db import connection
one_word = re.compile('^\w+$')
one_digit = re.compile('^\d+$')
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    
    sex = models.BooleanField()
    birthday = models.DateField(null=True)
    country = models.IntegerField(null=True)
    city = models.CharField(max_length=64, null=True)
    state = USStateField(null=True)
    zip_code = models.CharField(max_length=32, null=True)
    phone = PhoneNumberField(null=True)
    income = models.SmallIntegerField(null=True)
    ethnicity = models.SmallIntegerField(null=True)
    sexual_orientation = models.SmallIntegerField(null=True)
    relationship_status = models.SmallIntegerField(null=True)
    about = models.TextField(null=True)
    
    # tags
    political = models.ForeignKey(Tag, null=True, related_name='userprofile_set_political')
    religious = models.ForeignKey(Tag, null=True, related_name='userprofile_set_religious')
    education = models.ForeignKey(Tag, null=True,related_name='userprofile_set_education')
    work = models.ForeignKey(Tag, null=True,related_name='userprofile_set_work')
    interests = models.ManyToManyField(Tag, related_name='userprofile_set_interests')
    music = models.ManyToManyField(Tag, related_name='userprofile_set_music')
    tv = models.ManyToManyField(Tag, related_name='userprofile_set_tv')
    books = models.ManyToManyField(Tag, related_name='userprofile_set_books')
    movies = models.ManyToManyField(Tag, related_name='userprofile_set_movies')
    
    def get_tags_like(self, like, type, limit, many_to_many):
        if not one_digit.match(limit):
            limit = 10

        cursor = connection.cursor()
        if one_word.match(type):
            if many_to_many:
                cursor.execute("SELECT name, COUNT(*) as frequency FROM pollster_tag t, pollster_userprofile_" + type + " up WHERE t.id=up.tag_id AND name like %s GROUP BY name ORDER BY frequency DESC LIMIT " + limit + ";", [like + '%'])
            else:
                cursor.execute("SELECT name, COUNT(*) as frequency FROM pollster_tag t, pollster_userprofile up WHERE t.id=up." + type + "_id AND name like %s GROUP BY name ORDER BY frequency DESC LIMIT " + limit + ";", [like + '%'])
            rows = cursor.fetchall()
            return rows
        
class ScreenName(models.Model):
    screen_name = models.CharField(max_length=64)
    service = models.SmallIntegerField()
    user_profile = models.ForeignKey(UserProfile)

