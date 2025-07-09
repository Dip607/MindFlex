from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileForm
from .models import Profile
from django.contrib import messages

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed

@csrf_exempt
def custom_logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    elif request.method == 'GET':
        logout(request)
        return redirect('home')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
def home(request):
    return render(request, 'core/home.html')

def signup_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request, 'core/signup.html', {'user_form': user_form, 'profile_form': profile_form})

def login_view(request):
    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'core/login.html', {'form': form})

@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('home')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def matches(request):
    return render(request, 'core/matches.html')
