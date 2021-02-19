"""File for Model for Comments"""
from django.db import models


class Comment(models.Model):
    """Model for Comments"""

    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("Rareuser", on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
