from django.db import models
from django.contrib.auth.models import User


class Rareuser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150)
    profile_image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    created_on = models.DateField(auto_now=False, auto_now_add=False)
    active = models.BooleanField()
