from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    budget = models.IntegerField()
    cleanliness = models.IntegerField()
    sleep_schedule = models.CharField(max_length=20)
    introvert_extrovert = models.CharField(max_length=20)
    bio = models.TextField()
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username
