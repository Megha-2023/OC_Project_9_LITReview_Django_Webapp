from django import forms
from django.forms.widgets import FileInput
from . import models


class TicketForm(forms.ModelForm):
    """ Class to create Ticket form"""
    class Meta:
        """ meta class"""
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'image': FileInput(),
        }


class ReviewForm(forms.ModelForm):
    """ Class to create Review form"""
    class Meta:
        """ meta class"""
        model = models.Review
        CHOICES = [
            (i, i) for i in range(0, 6)
        ]
        widgets = {
            'rating': forms.RadioSelect(choices=CHOICES)
        }
        fields = ['headline', 'rating', 'body']


class FollowUsersForm(forms.ModelForm):
    """ Class to create user folllow form"""
    class Meta:
        """ meta class"""
        model = models.UserFollows
        fields = ['followed_user']
