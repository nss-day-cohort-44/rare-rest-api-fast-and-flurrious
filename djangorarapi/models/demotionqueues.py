"""File for Model for Demotion Queues"""
from django.db import models


class Demotionqueue(models.Model):
    """Model for Demotion Queues"""

    action = models.CharField(max_length=150)
    admin = models.ForeignKey("Rareuser", related_name="administrator", on_delete=models.CASCADE)
    approver_one = models.ForeignKey("Rareuser", related_name="approver", on_delete=models.CASCADE)
