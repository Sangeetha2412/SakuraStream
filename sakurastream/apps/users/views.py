from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User
from .forms import RegisterForm, LoginForm, ProfileUpdateForm


def register(request):
    if request.user.is_authenticated:
        return redirect('anime:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to SakuraStream! Your journey begins now.')
            return redirect('anime:home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('anime:home')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('anime:home')


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    watchlist = profile_user.watchlist.select_related('anime').order_by('-updated_at')[:10]
    reviews = profile_user.reviews.select_related('anime').order_by('-created_at')[:6]
    achievements = profile_user.achievements.all()
    activities = profile_user.activities.all()[:20]

    stats = {
        'completed': profile_user.watchlist.filter(status='completed').count(),
        'watching': profile_user.watchlist.filter(status='watching').count(),
        'plan_to_watch': profile_user.watchlist.filter(status='plan_to_watch').count(),
        'dropped': profile_user.watchlist.filter(status='dropped').count(),
        'reviews': profile_user.reviews.count(),
    }

    context = {
        'profile_user': profile_user,
        'watchlist': watchlist,
        'reviews': reviews,
        'achievements': achievements,
        'activities': activities,
        'stats': stats,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('users:profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})
