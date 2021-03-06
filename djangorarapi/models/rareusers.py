from django.db import models
from django.contrib.auth.models import User

class Rareuser(models.Model):
    """Model for Rare Users"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, null=True)
    profile_image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None, null=True)
    created_on = models.DateField(auto_now=False, auto_now_add=True, null=True)
