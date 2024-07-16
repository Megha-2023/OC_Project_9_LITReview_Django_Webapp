from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def feed_home_page(request):
    return render(request, 'feed/home.html')


def request_review_ticket(request):
    return render(request, 'feed/create_ticket.html')

