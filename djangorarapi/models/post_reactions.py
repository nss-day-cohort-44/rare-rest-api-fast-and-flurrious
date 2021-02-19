"""File for Model for Post-Reaction relationships"""
from django.db import models


class Post_Reaction(models.Model):
    """Model for Post-Reaction relationships"""

    user = models.ForeignKey("Rareuser", on_delete=models.CASCADE)
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
