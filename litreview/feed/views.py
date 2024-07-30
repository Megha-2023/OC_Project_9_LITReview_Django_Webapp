from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from feed.forms import TicketForm
from feed.models import Ticket


@login_required
def feed_home_page(request):
    tickets = Ticket.objects.all().order_by('-time_created').values()
    return render(request, 'feed/home.html', {'tickets': tickets})


def create_ticket(request):
    if request.method == 'POST':

        ticket_form = TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    else:
        ticket_form = TicketForm()

    return render(request, 'feed/create_ticket.html', {'form': ticket_form})

