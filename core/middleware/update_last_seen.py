# middleware/update_last_seen.py
from django.utils.timezone import now

class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.profile.last_seen = now()
            request.user.profile.save(update_fields=['last_seen'])
        return self.get_response(request)
