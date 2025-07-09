from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileForm
from .models import Profile
from django.contrib import messages
from .utils import find_top_matches_for_user, get_coordinates
from django.db.models import Avg
from .models import Feedback

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed
from .utils import find_top_matches_for_user

from .models import Message
from django.contrib.auth.models import User

@login_required
def profile_detail_view(request, user_id):
    from django.shortcuts import get_object_or_404
    from .models import Profile
    from django.contrib.auth.models import User
    from django.db.models import Avg

    user_obj = get_object_or_404(User, id=user_id)
    profile = user_obj.profile
    avg_rating = user_obj.received_feedback.aggregate(Avg('rating'))['rating__avg'] if hasattr(user_obj, 'received_feedback') else None

    return render(request, 'core/profile_detail.html', {
        'profile': profile,
        'avg_rating': avg_rating,
    })
    
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

from django.db.models import Avg
from .models import Feedback  # Assuming you have a Feedback model
from geopy.geocoders import Nominatim

def geocode_city(city):
    geolocator = Nominatim(user_agent="roommate-app")
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    return None, None

@login_required
def matches(request):
    user = request.user
    matches = find_top_matches_for_user(user)  # All matches with scores

    # Filter form
    gender = request.GET.get('gender')
    city = request.GET.get('city')
    max_budget = request.GET.get('budget')
    user_lat = float(user.profile.latitude or 22.5726)
    user_lon = float(user.profile.longitude or 88.3639)

    # 💡 Prepare filtered match list for display
    filtered_matches = []
    for match, score in matches:
        profile = match.profile
        if gender and profile.gender != gender:
            continue
        if city and city.lower() not in profile.city.lower():
            continue
        if max_budget:
            try:
                if profile.budget > int(max_budget):
                    continue
            except ValueError:
                pass
        filtered_matches.append((match, score))

    # ✅ Show ALL markers on map, not just filtered ones
    match_coords = []
    for match, score in matches:  # <--- Use full list here, not filtered_matches
        p = match.profile
        if p.latitude and p.longitude:
            match_coords.append({
                'user': match,
                'score': score,
                'city': p.city,
                'lat': p.latitude,
                'lon': p.longitude,
                'profile_pic': p.profile_pic.url if p.profile_pic else None,
            })

    context = {
        'matches': filtered_matches,  # only filtered list shown
        'match_coords': match_coords,  # all users shown on map
        'user_lat': user_lat,
        'user_lon': user_lon,
    }

    return render(request, 'core/matches.html', context)
