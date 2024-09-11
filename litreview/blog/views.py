import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
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

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj,
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
def post_review_to_ticket(request, tid):
    review_form = forms.ReviewForm()
    if tid:
        ticket = get_object_or_404(models.Ticket, id=tid)
        context = {'ticket': ticket,
                   'review_form': review_form}

    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket_id = ticket.id
            review.save()
        return redirect('home')
 
    return render(request, 'blog/post_review_to_ticket.html', context=context)


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
            else:
                # if already follow, show alert box 
                context = {
                    'user_exists': user_exists,
                    'already_follows': True,
                    'followed_user': followed_username,
                    'all_followed_users': all_followed_usernames,
                    'all_following_users': all_following_usernames
                }

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


@login_required
def own_posts(request):
    tickets = models.Ticket.objects.filter(Q(user_id=request.user.id))
    reviews = models.Review.objects.filter(Q(user_id=request.user.id))

    posts = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True
    )
    context = {'posts': posts}
    
    return render(request, 'blog/own_posts.html', context=context)


@login_required
def edit_(request, type_of_model: str, tid: int):
    if type_of_model == 'Ticket':
        ticket = get_object_or_404(models.Ticket, id=tid)
        ticket_form = forms.TicketForm(instance=ticket)

        if request.method == 'POST':

            ticket_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
            if ticket_form.is_valid():
                ticket_form.save()
                return redirect('own_posts')
        context = {'ticket_form': ticket_form,
                   'ticket': ticket}

    if type_of_model == 'Review':
        review = get_object_or_404(models.Review, id=tid)
        review_form = forms.ReviewForm(instance=review)
        ticket = get_object_or_404(models.Ticket, id=review.ticket_id)

        if request.method == 'POST':
            review_form = forms.ReviewForm(request.POST, request.FILES, instance=review)
            ticket = get_object_or_404(models.Ticket, id=review.ticket_id)
            if review_form.is_valid():
                review_form.save()
                return redirect('own_posts')

        context = {'review_form': review_form,
                   'ticket': ticket}

    return render(request, 'blog/edit_ticket.html', context=context)


@login_required
def ask_delete_confirm(request, type_of_model: str, tid: int):
    if type_of_model == 'Ticket':
        ticket = get_object_or_404(models.Ticket, id=tid)
        return render(request, 'blog/delete_ticket.html', {'ticket': ticket})
    
    if type_of_model == 'Review':
        review = get_object_or_404(models.Review, id=tid)
        return render(request, 'blog/delete_ticket.html', {'review': review})
    


@login_required
def delete_(request, type_of_model: str, tid: int):
    if type_of_model == 'Ticket':
        ticket = get_object_or_404(models.Ticket, id=tid)
        # if request.method == 'POST':
        # Remove image file of the ticket from media folder.
        if ticket.image:
            if os.path.isfile(ticket.image.path):
                os.remove(ticket.image.path)
        ticket.delete()
        return redirect('own_posts')
     
    if type_of_model == 'Review':
        review = get_object_or_404(models.Review, id=tid)
        # if request.method == 'POST':
        review.delete()
        return redirect('own_posts')
    
    return render(request, 'blog/delete_ticket.html')
