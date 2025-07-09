from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileForm
from .models import Profile
from django.contrib import messages
from .utils import find_top_matches_for_user, get_coordinates


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed
from .utils import find_top_matches_for_user

from .models import Message
from django.contrib.auth.models import User
@login_required  # Optional: remove if public
def all_users_view(request):
    profiles = Profile.objects.select_related('user').all()
    return render(request, 'core/all_users.html', {'profiles': profiles})
@login_required
def chat_view(request, user_id):
    other_user = User.objects.get(id=user_id)

    # Check if they are matched
    match_allowed = any(match[0] == other_user for match in find_top_matches_for_user(request.user))

    if not match_allowed:
        return render(request, 'core/not_allowed.html')

    if request.method == 'POST':
        msg = request.POST.get('message')
        if msg:
            Message.objects.create(sender=request.user, receiver=other_user, message=msg)

    messages_qs = Message.objects.filter(
        sender=request.user, receiver=other_user
    ) | Message.objects.filter(
        sender=other_user, receiver=request.user
    )
    messages_qs = messages_qs.order_by('timestamp')

    return render(request, 'core/chat.html', {
        'messages': messages_qs,
        'other_user': other_user
    })


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

            # ✅ Capture coordinates from hidden fields
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            if latitude and longitude:
                profile.latitude = latitude
                profile.longitude = longitude

            profile.save()

            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()

    return render(request, 'core/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
    
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
    user = request.user
    matches = find_top_matches_for_user(user)

    gender = request.GET.get('gender')
    city = request.GET.get('city')
    max_budget = request.GET.get('budget')

    # ✅ Apply filters
    if gender:
        matches = [m for m in matches if m[0].profile.gender == gender]
    if city:
        matches = [m for m in matches if city.lower() in m[0].profile.city.lower()]
    if max_budget:
        matches = [m for m in matches if m[0].profile.budget <= int(max_budget)]

    # ✅ Build marker data
    match_coords = []
    for match, score in matches:
        profile = match.profile  # <-- FIXED: define p properly here
        if profile.latitude and profile.longitude:
            match_coords.append({
                'user': match,
                'score': score,
                'city': profile.city,
                'lat': profile.latitude,
                'lon': profile.longitude,
                'profile_pic': profile.profile_pic.url if profile.profile_pic else None,
            })

    context = {
        'matches': matches,
        'match_coords': match_coords,
        'user_lat': user.profile.latitude,
        'user_lon': user.profile.longitude,
    }

    return render(request, 'core/matches.html', context)
