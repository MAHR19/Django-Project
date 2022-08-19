import datetime
from distutils.command.upload import upload
import time
from django.shortcuts import get_object_or_404
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum
from django import forms    

def date_limit():#One Week for each Question POll
    return timezone.now()+ datetime.timedelta(days=7)


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    email = models.EmailField(default = 'someone@sample.com')


class Question(models.Model):

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    deadline = models.DateTimeField(default=date_limit)

    def is_out_of_time(self):
        if timezone.now()>=self.deadline:
            obj=get_object_or_404(Question, name=self.question_text)
            obj.delete()

    def total_votes(self):
        return Choice.objects.aggregate(Sum('votes'))['votes__sum']


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

    def __str__(self):
        return self.choice_text
