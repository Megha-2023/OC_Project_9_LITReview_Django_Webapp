from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from . import models

@login_required
def home_page(request):
    tickets = models.Ticket.objects.all().order_by('-time_created')
    return render(request, 'blog/home.html', {'tickets': tickets})
    # .prefetch_related('user')

@login_required
def create_ticket(request):
    if request.method == 'POST':

        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    else:
        ticket_form = forms.TicketForm()

    return render(request, 'blog/create_ticket.html', {'form': ticket_form})

@login_required
def create_review(request):
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review_form = forms.ReviewForm(request.POST, request.FILES)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.save()
                return redirect('home')
    else:
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()
    
    context = {'ticket_form': ticket_form,
               'review_form': review_form}
    return render(request, 'blog/create_review.html', context=context)
