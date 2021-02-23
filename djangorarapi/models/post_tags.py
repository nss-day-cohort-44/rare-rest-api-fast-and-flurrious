"""File for Model for Post-Reaction relationships"""
from django.db import models


class Post_Tag(models.Model):
    """Model for Post-Reaction relationships"""

    # 'related_name' defines the property to be joined as a virtual property in the Post model
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name="tags")
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
