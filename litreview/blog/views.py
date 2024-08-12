from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . import forms
from . import models
from authentication.models import User

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


@login_required
def follow_users(request):

    all_following_usernames = models.UserFollows.objects.values_list('following_user__username').filter(followed_user=request.user)
    
    all_followed_usernames = models.UserFollows.objects.values_list('followed_user__username').filter(following_user=request.user)
    # User.objects.filter(id=models.UserFollows.objects.filter(following_user=request.user))
    
    user_exists = True
    context = {
        'user_exists': user_exists,
        'all_followed_users': all_followed_usernames,
        'all_following_users': all_following_usernames
    }
    if request.method == 'POST':
        # following_user = request.user
        followed_username = request.POST.get('followed_user')
        try:
            followed_user_obj = User.objects.get(username=followed_username)
            
            is_following = models.UserFollows.objects.filter(
                        following_user=request.user,
                        followed_user=followed_user_obj).exists()
        
            if not is_following:
                user_follow_obj = models.UserFollows(following_user=request.user, followed_user=followed_user_obj)
                user_follow_obj.save()

            # context = {
            #    'user_exists': user_exists,
            #    'all_followed_users': all_followed_usernames,
            #    'all_following_users': all_following_usernames
            #}
        except User.DoesNotExist:
            user_exists = False
            context = {
                'user_exists': user_exists,
                'followed_user': followed_username,
                'all_followed_users': all_followed_usernames,
                'all_following_users': all_following_usernames
            }
    
    return render(request, 'blog/follow_users.html', context=context)


def unfollow_user(request, user_name):
    if user_name:
        user_id = User.objects.get(username=user_name).id
        models.UserFollows.objects.filter(followed_user=user_id).delete()
    
    # follow_users(request)
    return redirect('follow_users')
