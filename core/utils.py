import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .models import Profile
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="roommate_app")

def get_coordinates(city):
    try:
        location = geolocator.geocode(city)
        if location:
            return (location.latitude, location.longitude)
    except GeocoderTimedOut:
        pass
    return None

def encode_profile(profile):
    sleep_map = {"Early": 0, "Night Owl": 1}
    personality_map = {"Introvert": 0, "Extrovert": 1}

    return np.array([
        profile.budget,
        profile.cleanliness,
        sleep_map.get(profile.sleep_schedule, 0),
        personality_map.get(profile.introvert_extrovert, 0),
    ])

def find_top_matches_for_user(user, top_n=5):
    all_profiles = Profile.objects.exclude(user=user)
    user_vector = encode_profile(user.profile).reshape(1, -1)

    scores = []
    for profile in all_profiles:
        try:
            vector = encode_profile(profile).reshape(1, -1)
            score = cosine_similarity(user_vector, vector)[0][0]
            scores.append((profile.user, round(score * 100, 2)))
        except:
            continue

    sorted_matches = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_matches[:top_n]