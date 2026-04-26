from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import UserProfile
from .forms import (
    UserRegistrationForm,
    UserUpdateForm,
    ProfileUpdateForm,
    EmailOrUsernameAuthenticationForm,
)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = EmailOrUsernameAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Allow login via username OR email in the same field
            User = get_user_model()
            user_obj = User.objects.filter(
                Q(username__iexact=identifier) | Q(email__iexact=identifier)
            ).first()

            username_for_auth = user_obj.username if user_obj else identifier
            user = authenticate(username=username_for_auth, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_short_name() or user.username}!')
                return redirect('store:home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = EmailOrUsernameAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

from django.contrib.auth import logout as auth_logout

def user_logout(request):
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('store:home')

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def orders(request):
    # This would typically show user's order history
    orders = request.user.orders.all()
    context = {
        'orders': orders,
    }
    return render(request, 'users/orders.html', context)
