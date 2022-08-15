from django import forms
from django.contrib.auth.models import User
from polls.models import UserProfileInfo

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())


    class Meta():
        model= User
        fields = ('username','email','password')



class UserProfileData(forms.ModelForm):
    class Meta():
        models=UserProfileInfo
        fields=('profile_pic')