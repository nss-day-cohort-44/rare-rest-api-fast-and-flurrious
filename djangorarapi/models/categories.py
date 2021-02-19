"""File for Model for Categories"""
from django.db import models


class Category(models.Model):
    """Model for Categories"""

    label = models.CharField(max_length=50)
