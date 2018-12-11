from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse
from djangoforms.models import Tweet, Author, Notification
from djangoforms.forms import AddTweet, SignupForm, LoginForm
from datetime import datetime
import re

# TODOS
# only show tweets from followed users
# notifications go away once viewed


@login_required()
def all_tweets(request):
    html = 'all_tweets.html'
    user = Author.objects.filter(user_id=request.user.id).first()
    tweets = Tweet.objects.order_by('-timestamp')
    return render(request, html, {'data': {
        'tweets': tweets,
        'user': user,
    }})


def tweet(request, tweet_id):
    results = Tweet.objects.filter(id=tweet_id).first()
    return render(request, 'tweet.html', {'data': results})


def author(request, author_id):
    author = Author.objects.filter(id=author_id).first()
    tweets = Tweet.objects.filter(author=author).order_by('-timestamp')
    count = tweets.count()
    user = request.user
    notifications = Notification.objects.filter(user_mentioned=author)
    return render(request, 'author.html', {'data': {
        'author': author,
        'tweets': tweets,
        'count': count,
        'user': user,
        'notifications': notifications
    }})


@login_required()
def add_tweet(request):
    html = 'add_tweet.html'
    form = None
    if request.method == 'POST':
        form = AddTweet(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Tweet.objects.create(
                body=data['body'],
                author=Author.objects.filter(id=data['author']).first(),
                timestamp=datetime.now()
            )
            for mention in re.findall(r'@([^\n ]*)', data['body']):
                Notification.objects.create(
                    user_mentioned=Author.objects.filter(name=mention).first(),
                    tweet=Tweet.objects.filter(body=data['body']).first(),
                )
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = AddTweet(user=request.user)
    return render(request, html, {'form': form})


def signup_view(request):

    html = 'signup.html'
    form = SignupForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'], data['email'], data['password'])
        Author.objects.create(
            name=user.username,
            user=user,
        )
        login(request, user)
        return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {'form': form})


def login_view(request):
    html = 'login.html'
    form = LoginForm(None or request.POST)
    if form.is_valid():
        next = request.POST.get('next')
        data = form.cleaned_data
        user = authenticate(
            username=data['username'], password=data['password'])
        if user is not None:
            login(request, user)
            if next:
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required()
def follow(request, author_id):
    # author = Author.objects.filter(id=author_id).first()
    user = Author.objects.filter(user_id=request.user.id).first()
    user.following.add(author_id)
    print(user.following.all())
    return HttpResponseRedirect('/author/' + str(author_id))


@login_required()
def unfollow(request, author_id):
    user = Author.objects.filter(user_id=request.user.id).first()
    user.following.remove(author_id)
    print(user.following.all())
    return HttpResponseRedirect('/author/' + str(author_id))
