"""File for Model for Subscriptions"""
from django.db import models


class Subscription(models.Model):
    """Model for Subscriptions"""

    follower = models.ForeignKey("Rareuser", related_name="follower", on_delete=models.CASCADE)
    author = models.ForeignKey("Rareuser", related_name="author", on_delete=models.CASCADE)
    created_on = models.DateField(auto_now=False, auto_now_add=True)
    ended_on = models.DateField(auto_now=False, auto_now_add=False, null=True)
