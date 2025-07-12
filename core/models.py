from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

   
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    tags = models.TextField(blank=True, null=True)
    budget = models.IntegerField(null=True, blank=True)
    cleanliness = models.IntegerField(null=True, blank=True, default="yes")
    sleep_schedule = models.CharField(max_length=20, null=True, blank=True)
    introvert_extrovert = models.CharField(max_length=20, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    college_id = models.FileField(upload_to='college_ids/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    last_seen = models.DateTimeField(default=now)
    def __str__(self):
        return f"{self.user.username}'s Profile"
class Feedback(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_feedback')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_feedback')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)