from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
from . import forms
from . import models
from authentication.models import User

@login_required
def home_page(request):
    followed_user_ids = models.UserFollows.objects.values_list('followed_user__id').filter(
                                                                            following_user=request.user)
    
    tickets = models.Ticket.objects.filter(Q(user_id__in=followed_user_ids) | Q(user_id=request.user.id))

    reviews = models.Review.objects.filter(Q(user_id__in=followed_user_ids) | Q(user_id=request.user.id))
    
    not_reviewed_by_user = []
    for ticket in tickets:
        user_flag = None
        if ticket.user_id == request.user.id:
            user_flag = 1
        for review in reviews:
            if review.ticket_id == ticket.id:
                user_flag = 1
        if user_flag is None:
            not_reviewed_by_user.append(ticket)
    
    posts = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {'posts': posts,
               'not_reviewed_by_user': not_reviewed_by_user}
    
    return render(request, 'blog/home.html', context=context)


@login_required
def create_ticket(request, post_review=None):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()
    if post_review == 'True':
        context = {'post_review': post_review,
                    'ticket_form': ticket_form,
                    'review_form': review_form}
    else:
        context = {'ticket_form': ticket_form}

    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket_id = ticket.id
                review.save()
        return redirect('home')

    return render(request, 'blog/create_ticket.html', context=context)
    

@login_required
def follow_users(request):
    # get usernames of all users who follows current user
    all_following_usernames = models.UserFollows.objects.values_list('following_user__username').filter(
                                                                            followed_user=request.user)
    # get usernames of all users to whom current user follows
    all_followed_usernames = models.UserFollows.objects.values_list('followed_user__username').filter(
                                                                            following_user=request.user)
    
    user_exists = True
    context = {
        'user_exists': user_exists,
        'all_followed_users': all_followed_usernames,
        'all_following_users': all_following_usernames
    }
    if request.method == 'POST':
        # get username entered in text box
        followed_username = request.POST.get('followed_user')
        try:
            # check whether entered username exists or not
            followed_user_obj = User.objects.get(username=followed_username)

            # check current user already follows the user entered in the textbox
            is_following = models.UserFollows.objects.filter(
                        following_user=request.user,
                        followed_user=followed_user_obj).exists()
            # if not, then save entry in table
            if not is_following:
                user_follow_obj = models.UserFollows(following_user=request.user, followed_user=followed_user_obj)
                user_follow_obj.save()

        except User.DoesNotExist:
            user_exists = False
            context = {
                'user_exists': user_exists,
                'followed_user': followed_username,
                'all_followed_users': all_followed_usernames,
                'all_following_users': all_following_usernames
            }

    return render(request, 'blog/follow_users.html', context=context)


@login_required
def unfollow_user(request, user_name):
    if user_name:
        user_id = User.objects.get(username=user_name).id
        models.UserFollows.objects.filter(followed_user=user_id).delete()
    
    return redirect('follow_users')
