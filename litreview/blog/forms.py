from django import forms
from django.forms.widgets import FileInput
from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'image': FileInput(),
        }


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        CHOICES = [
            (i, i) for i in range(0, 6)
        ]
        widgets = {
            'rating': forms.RadioSelect(choices=CHOICES)
        }
        fields = ['headline', 'rating', 'body']


class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ['followed_user']
