"""File for Model for Subscriptions"""
from django.db import models


class Tag(models.Model):
    """Model for Subscriptions"""

    label = models.CharField(max_length=50)
