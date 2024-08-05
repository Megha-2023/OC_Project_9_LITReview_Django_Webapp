from django import forms
from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


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
