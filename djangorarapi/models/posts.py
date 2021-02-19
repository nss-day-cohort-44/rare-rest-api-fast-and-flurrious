"""File for Model for Posts"""
from django.db import models


class Post(models.Model):
    """Model for Posts"""

    user = models.ForeignKey("Rareuser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    publication_date = models.DateField(auto_now=False, auto_now_add=True)
    profile_image_url = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    content = models.CharField(max_length=1500)
    approved = models.BooleanField()
