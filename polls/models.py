import datetime
from distutils.command.upload import upload
import time
from django.db import models
from django.utils import timezone
#from django.contrib.auth import User
from django.contrib.auth.models import User
from django.db.models import Sum


def date_limit():#One Week for each Question POll
    return timezone.now()+ datetime.timedelta(days=7)


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    
    
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    deadline = models.DateTimeField(default=date_limit)

    def total_votes(self):
        sum = Choice.objects.aggregate(Sum('votes'))['votes__sum']
        #return self.choice_set.aggregate(Sum('votes'))['votes__sum']
        return sum

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


    
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    """def total(self):
        return sum([self.votes for self.choice_text in self.objects.all()])"""
        

    def __str__(self):
        return self.choice_text
